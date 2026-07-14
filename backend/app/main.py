from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.api.routes import chat, menu, orders, user, voice, auth
from app.db.session import engine
from app.models import Base
from app.session.store import session_store
from app.core.config import settings
import os

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="MoodBowl AI System")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await session_store.connect()

# Include Routers
app.include_router(chat.router, prefix="/api")
app.include_router(menu.router, prefix="/api")
app.include_router(orders.router, prefix="/api")

app.include_router(user.router, prefix="/api")
app.include_router(voice.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

# Serve Static Files
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app.mount("/", StaticFiles(directory=static_path, html=True), name="static")
