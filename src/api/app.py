import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.chat import router as chat_router
from src.api.routes.health import router as health_router


def _allowed_origins() -> list[str]:
    raw = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
    return [item.strip() for item in raw.split(",") if item.strip()]


app = FastAPI(title="Search Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(chat_router)
