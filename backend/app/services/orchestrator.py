import re
import asyncio
import time
import json
from typing import Dict, Any
import google.generativeai as genai
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.response_formatter import (
    format_clarification, format_recommendations,
    format_order_summary, format_history,
    format_preference_update, format_fallback
)
from app.schemas import WaiterChatRequest, WaiterChatResponse
from app.services.recommender import recommender
from app.core.config import settings
from app.schemas import ChatRequest, ChatResponse
from app.tools import order_tools, user_tools, menu_tools
from app.session.store import session_store

class Orchestrator:
    def __init__(self):
        if not settings.MOCK_MODE:
            genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def process_message(self, db: AsyncSession, request: ChatRequest) -> ChatResponse:
        start_time = time.time()
        
        # Load session
        session_data = await session_store.get_session(request.session_id)
        
        # 1. Intent Detection (Pass 1: Regex)
        intent = self._detect_intent_regex(request.message)
        
        # 2. Pass 2: LLM Intent (if needed)
        if intent == "ambiguous":
            intent = await self._detect_intent_llm(request.message)

        mood_info = None
        recommendations = []
        reply = format_fallback()

        # 3. Routing
        if intent == "browsing":
            from app.schemas import MoodInfo
            mood_info = MoodInfo(mood="neutral", mood_id="neutral", energy_level="medium", craving_type="balanced", confidence=1.0)
            budget = session_data.get("budget")
            allergies = session_data.get("allergies")
            recommendations = await recommender.get_recommendations(db, request.user_id, mood_info.model_dump(), context_override=None, query_text=request.message)
            reply = format_recommendations(recommendations, mood_info.model_dump())
            
            # Save state for potential ordering
            if recommendations:
                session_data["last_recommendations"] = recommendations
                session_data["last_mood"] = mood_info.model_dump()
        
        elif intent == "ordering":
            # Very basic ordering logic for MVP: take the first item from last recs, or mock
            if "last_recommendations" in session_data and session_data["last_recommendations"]:
                item_id = session_data["last_recommendations"][0]["id"]
                mood = session_data.get("last_mood", {})
                order_result = await order_tools.place_order(db, request.user_id, item_id, mood)
                reply = format_order_summary(order_result)
                # Clear recommendations after order
                session_data["last_recommendations"] = []
            else:
                reply = "I'm not sure what you want to order. Could you tell me what you're craving first?"
        
        elif intent == "history":
            history = await order_tools.get_order_history(db, request.user_id)
            reply = format_history(history)
            
        elif intent == "preference_update":
            # For simplicity, just updating a dummy preference
            # In a real app we'd extract the entities (e.g., 'vegetarian')
            await user_tools.update_preference(db, request.user_id, {"dietary_pref": "vegetarian"})
            reply = format_preference_update()

        elif intent == "ambiguous":
            reply = format_fallback()

        # Save session
        await session_store.save_session(request.session_id, session_data)

        latency_ms = int((time.time() - start_time) * 1000)
        
        return ChatResponse(
            intent=intent,
            mood=mood_info,
            recommendations=recommendations,
            reply=reply,
            latency_ms=latency_ms
        )

    def _detect_intent_regex(self, message: str) -> str:
        msg = message.lower()
        if any(w in msg for w in ["recommend", "hungry", "eat", "food", "feeling", "mode", "budget", "price", "dollars", "happy", "sad", "stressed", "tired"]): return "browsing"
        if any(w in msg for w in ["order", "buy", "take it", "yes", "confirm"]): return "ordering"
        if any(w in msg for w in ["history", "past", "last time"]): return "history"
        if any(w in msg for w in ["preference", "allergy", "diet", "vegetarian", "vegan"]): return "preference_update"
        return "ambiguous"

    async def _detect_intent_llm(self, message: str) -> str:
        if settings.MOCK_MODE:
            return "browsing" # Default mock
            
        prompt = f"""
        Classify the intent of this user message into EXACTLY one of the following 5 classes:
        [browsing, ordering, preference_update, history, ambiguous]
        Message: "{message}"
        Return just the class name as plain text. Do not return JSON.
        """
        try:
            # Temperature=0.0 as per spec
            generation_config = genai.types.GenerationConfig(temperature=0.0)
            response = await asyncio.wait_for(
                asyncio.to_thread(self.model.generate_content, prompt, generation_config=generation_config),
                timeout=settings.GEMINI_TIMEOUT_SECONDS
            )
            intent = response.text.strip().lower()
            if intent in ["browsing", "ordering", "preference_update", "history", "ambiguous"]:
                return intent
            return "ambiguous"
        except Exception:
            return "ambiguous"

    async def _generate_waiter_response(self, history: list, session_data: dict, current_message: str = "", user_context: str = "") -> dict:
        if len(history) == 0:
            return {
                "intent": "CLARIFY",
                "value": None,
                "detected_mood": "NEUTRAL",
                "voice_response": "Welcome to MoodBowl! I'm your AI assistant. Tell me, what are you in the mood for today?"
            }

        prompt = f"""
You are the MoodBowl Voice Controller. Your job is to translate user speech into a JSON command for a food ordering app.

Available Actions:
- Maps: Move to 'home', 'explore', 'cart', 'profile', or 'favorites'.
- ADD_TO_CART: Add a specific item.
- ADD_TO_FAVORITES: Mark an item as favorite.
- SET_MOOD: Update the user's current mood based on their tone or words.
- CLARIFY: If the user's intent is unclear, ask a helpful question.

Constraint: 
- If the user's intent is unclear, respond with intent: "CLARIFY" and a helpful question.
- ALWAYS output ONLY valid JSON.

Output Format:
{{
  "intent": "ACTION_NAME",
  "value": "ITEM_OR_PAGE_NAME",
  "detected_mood": "HAPPY|STRESSED|TIRED|CELEBRATING|NEUTRAL",
  "voice_response": "Short, natural confirmation phrase"
}}

User Context: {user_context}
Session State: {json.dumps(session_data)}

History:
"""
        for msg in history:
            role = "Waiter" if msg['role'] == 'model' else "Customer"
            prompt += f"{role}: {msg['content']}\n"
        
        prompt += f"Customer: {current_message}\nWaiter: "

        if settings.MOCK_MODE:
            return {
                "intent": "CLARIFY",
                "value": "Mock",
                "detected_mood": "HAPPY",
                "voice_response": "This is a mock response."
            }

        fallback = {
            "intent": "CLARIFY",
            "value": None,
            "detected_mood": "NEUTRAL",
            "voice_response": "I didn't quite catch that. Could you repeat?"
        }

        try:
            generation_config = genai.types.GenerationConfig(temperature=0.1)
            response = await asyncio.wait_for(
                asyncio.to_thread(self.model.generate_content, prompt, generation_config=generation_config),
                timeout=settings.GEMINI_TIMEOUT_SECONDS
            )
            raw_text = response.text.strip()
            if raw_text.startswith("```json"): raw_text = raw_text[7:]
            if raw_text.startswith("```"): raw_text = raw_text[3:]
            if raw_text.endswith("```"): raw_text = raw_text[:-3]
            
            data = json.loads(raw_text.strip())
            print(f"Single-Stream AI Response: {data}")
            return data
        except Exception as e:
            print("AI Error:", str(e))
            return fallback


    async def waiter_greet(self, db: AsyncSession, request: WaiterChatRequest) -> WaiterChatResponse:
        session_data = await session_store.get_session(request.session_id)
        
        from app.models import User
        from sqlalchemy import select
        stmt = select(User).where(User.user_id == request.user_id)
        u_res = await db.execute(stmt)
        user = u_res.scalar_one_or_none()
        
        user_context = ""
        if user:
            user_context = f"Known permanent preferences for this user -> Name: {user.name}, Allergies: {user.allergens}, Maximum Budget: {user.budget_preference}. Acknowledge these if relevant."
            
        session_data['waiter_history'] = []
        
        waiter_obj = await self._generate_waiter_response(session_data['waiter_history'], session_data, user_context=user_context)
        reply = waiter_obj.get("voice_response", "Welcome to MoodBowl!")
        
        session_data['waiter_history'].append({'role': 'model', 'content': reply})
        await session_store.save_session(request.session_id, session_data)
        
        return WaiterChatResponse(
            intent=waiter_obj.get("intent", "CLARIFY"),
            value=waiter_obj.get("value"),
            detected_mood=waiter_obj.get("detected_mood", "NEUTRAL"),
            voice_response=reply,
            recommendations=[]
        )

    async def waiter_message(self, db: AsyncSession, request: WaiterChatRequest) -> WaiterChatResponse:
        session_data = await session_store.get_session(request.session_id)
        history = session_data.get('waiter_history', [])
        
        from app.models import User
        from sqlalchemy import select
        stmt = select(User).where(User.user_id == request.user_id)
        u_res = await db.execute(stmt)
        user = u_res.scalar_one_or_none()
        
        user_context = ""
        if user:
            user_context = f"Preferences: Name: {user.name}, Allergies: {user.allergens}, Budget: {user.budget_preference}."

        if request.message:
            history.append({'role': 'user', 'content': request.message})
            
        waiter_obj = await self._generate_waiter_response(history, session_data, current_message=request.message, user_context=user_context)
        reply = waiter_obj.get("voice_response", "Understood.")
        
        history.append({'role': 'model', 'content': reply})
        
        # Keep history bounded
        if len(history) > 10:
            history = history[-10:]
            
        session_data['waiter_history'] = history
        await session_store.save_session(request.session_id, session_data)
        
        recommendations = []
        
        extracted_mood = waiter_obj.get("detected_mood", "NEUTRAL").lower()
        extracted_value = waiter_obj.get("value", "")
        
        from app.schemas import MoodInfo
        mood_info = MoodInfo(
            mood=extracted_mood,
            mood_id=extracted_mood,
            energy_level="medium",
            craving_type="any",
            confidence=1.0
        )
        
        context_override = session_data.get("temp_constraints", {})
        
        if extracted_value and isinstance(extracted_value, str):
            val_lower = extracted_value.lower()
            if "under 200" in val_lower or "budget" in val_lower:
                import re
                match = re.search(r'under\s*(\d+)', val_lower)
                if match:
                    context_override['budget'] = float(match.group(1))
            
            if "veg" in val_lower:
                context_override['dietary'] = ["vegetarian"]
            if "peanut" in val_lower:
                context_override['allergies'] = ["peanut"]
                
        session_data["temp_constraints"] = context_override

        recommendations = await recommender.get_recommendations(
            db, 
            request.user_id, 
            mood_info.model_dump(), 
            context_override=context_override, 
            query_text=extracted_value
        )
        
        if recommendations:
            from app.tools.location_tools import get_restaurant_status, calculate_delivery_estimate
            active_recs = []
            for rec in recommendations:
                resto_id = rec.get("restaurant_id", 0)
                if resto_id and not get_restaurant_status(resto_id):
                    continue
                if rec.get("restaurant_name"):
                    rec["delivery_estimate"] = calculate_delivery_estimate("mock", "mock")
                active_recs.append(rec)
            recommendations = active_recs
        
        if not recommendations and waiter_obj.get("intent") != "CLARIFY":
            reply = f"I'm sorry, I don't have matching food for '{extracted_mood}' with those exact rules right now, but how about a comforting Dal Makhani instead?"
             
        return WaiterChatResponse(
            intent=waiter_obj.get("intent", "CLARIFY"),
            value=waiter_obj.get("value"),
            detected_mood=waiter_obj.get("detected_mood", "NEUTRAL"),
            voice_response=reply,
            recommendations=recommendations
        )

    async def waiter_live_session(self, websocket, db: AsyncSession, user_id: int, session_id: str):
        import traceback
        try:
            print(f"DEBUG: WS Incoming Connection for User {user_id}")
            
            try:
                from google import genai
                from google.genai import types
                import asyncio
                import json
                print("DEBUG: Libraries imported successfully")
            except Exception as e:
                print(f"DEBUG: Import Error: {e}")
                await websocket.close(code=1011)
                return

            # 1. Fetch Context
            try:
                from app.models import User
                from sqlalchemy import select
                stmt = select(User).where(User.user_id == user_id)
                u_res = await db.execute(stmt)
                user = u_res.scalar_one_or_none()
                user_context = f"Name: {user.name}, Allergies: {user.allergens}, Maximum Budget: {user.budget_preference}" if user else "None"
                print(f"DEBUG: User context loaded: {user_context}")
            except Exception as e:
                print(f"DEBUG: DB Error: {e}")
                user_context = "None"

            instruction = "You are the MoodBowl Voice Controller. Be an empathetic culinary assistant. Respond in JSON."

            # 2. Setup New SDK Gemini Live Config
            print(f"DEBUG: Connecting to Gemini Live with API Key: {settings.GOOGLE_GEMINI_API_KEY[:5]}...")
            client = genai.Client(api_key=settings.GOOGLE_GEMINI_API_KEY)
            
            try:
                # Use standard model name format without models/ prefix
                async with client.aio.live.connect(model='gemini-2.0-flash-exp', config={'system_instruction': instruction}) as session:
                    print("DEBUG: Gemini Live Session successfully opened!")
                    
                    # Force an initial greeting
                    await session.send(input="Please say 'Welcome to MoodBowl!'", end_of_turn=True)
                    print("DEBUG: Initial greeting sent to Gemini")

                    async def recv_browser_send_gemini():
                        try:
                            while True:
                                message = await websocket.receive()
                                if message["type"] == "websocket.disconnect":
                                    print("DEBUG: WebSocket Disconnect received")
                                    break
                                    
                                if "text" in message:
                                    data = json.loads(message["text"])
                                    user_text = data.get("client_content", "")
                                    if user_text:
                                        print(f"DEBUG: Sending text to Gemini: {user_text}")
                                        await session.send(input=user_text, end_of_turn=True)
                                elif "bytes" in message:
                                    # Raw audio bytes from the mic (16kHz PCM)
                                    await session.send(input={"data": message["bytes"], "mime_type": "audio/pcm;rate=16000"})
                        except Exception as e:
                            print(f"DEBUG: recv_browser error: {e}")

                    async def recv_gemini_send_browser():
                        try:
                            async for response in session.receive():
                                if response.server_content and response.server_content.model_turn:
                                    for part in response.server_content.model_turn.parts:
                                        if part.text:
                                            payload = {"server_content": {"text": part.text}}
                                            await websocket.send_text(json.dumps(payload))
                                        elif part.inline_data:
                                            import base64
                                            encoded_audio = base64.b64encode(part.inline_data.data).decode('utf-8')
                                            payload = {"server_content": {"inline_data": encoded_audio}}
                                            await websocket.send_text(json.dumps(payload))
                        except Exception as e:
                            print(f"DEBUG: recv_gemini error: {e}")

                    await asyncio.gather(
                        recv_browser_send_gemini(),
                        recv_gemini_send_browser(),
                        return_exceptions=True
                    )
            except Exception as e:
                print(f"DEBUG: Gemini Connect/Session Error: {e}")
                with open("c:\\Users\\shrad\\Downloads\\moodbite\\gemini_error.txt", "w") as f:
                    traceback.print_exc(file=f)
                await websocket.send_text(json.dumps({"error": str(e)}))

        except Exception as e:
            print(f"DEBUG: Final Catch-All Error: {e}")
            with open("c:\\Users\\shrad\\Downloads\\moodbite\\ws_error.txt", "w") as f:
                traceback.print_exc(file=f)
            try:
                await websocket.close(code=1011)
            except:
                pass

orchestrator = Orchestrator()
