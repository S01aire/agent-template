from fastapi import APIRouter, Depends, HTTPException

from src.api.deps import get_chat_service
from src.schemas.chat import ChatResponse, ResumeRequest, SendRequest
from src.service.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/send", response_model=ChatResponse)
def send_message(payload: SendRequest, service: ChatService = Depends(get_chat_service)) -> ChatResponse:
    try:
        return service.send(session_id=payload.session_id, message=payload.message)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/resume", response_model=ChatResponse)
def resume_message(payload: ResumeRequest, service: ChatService = Depends(get_chat_service)) -> ChatResponse:
    try:
        return service.resume(
            session_id=payload.session_id,
            tool_use_id=payload.tool_use_id,
            answer=payload.answer,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
