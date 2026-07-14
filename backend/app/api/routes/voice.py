from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models import VoiceSample, Mood
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class MoodDetectionRequest(BaseModel):
    user_id: int
    text: Optional[str] = None
    voice_sample_id: Optional[int] = None

@router.post("/detect-mood")
async def detect_mood(payload: MoodDetectionRequest, db: AsyncSession = Depends(get_db)):
    # Mock AI Analysis Logic
    # In production, this would call Gemini or a local audio-to-text / sentiment model
    detected = "happy"
    if payload.text and "sad" in payload.text.lower():
        detected = "sad"
    
    return {
        "user_id": payload.user_id,
        "detected_mood": detected,
        "confidence": 0.85,
        "suggested_action": "recommend_food"
    }

@router.post("/voice-analysis")
async def voice_analysis(user_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    # 1. Save file to storage (Mock URL for now)
    audio_url = f"https://storage.moodbowl.app/voice/{user_id}/{file.filename}"
    
    # 2. Mock Audio Analysis
    detected_mood = "stressed"
    confidence = 0.92
    
    # 3. Create VoiceSample record
    sample = VoiceSample(
        user_id=user_id,
        detected_mood=detected_mood,
        confidence_score=confidence,
        audio_url=audio_url
    )
    db.add(sample)
    await db.commit()
    await db.refresh(sample)
    
    return sample
