from src.service.chat_service import ChatService
from src.session.memory_store import MemorySessionStore


_store = MemorySessionStore()
_chat_service = ChatService(_store)


def get_chat_service() -> ChatService:
    return _chat_service
