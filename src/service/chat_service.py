from __future__ import annotations

from src.agent.agent_factory import get_main_agent
from src.model.event import EventType
from src.schemas.chat import AwaitHumanResponse, ChatResponse, FinalResponse
from src.session.memory_store import MemorySessionStore


class ChatService:
    def __init__(self, store: MemorySessionStore, session_ttl_seconds: int = 3600) -> None:
        self.store = store
        self.session_ttl_seconds = session_ttl_seconds

    def send(self, session_id: str, message: str) -> ChatResponse:
        state = self.store.get_or_create(session_id, get_main_agent)
        with state.lock:
            state.messages.append({"role": "user", "content": message})
            event = state.agent.agent_loop(state.messages)
            return self._to_response(state, event)

    def resume(self, session_id: str, tool_use_id: str, answer: str) -> ChatResponse:
        state = self.store.get(session_id)
        if state is None:
            raise ValueError("session_id not found")

        with state.lock:
            if state.pending_tool_use_id is None:
                raise ValueError("session is not waiting for human input")
            if state.pending_tool_use_id != tool_use_id:
                raise ValueError("tool_use_id mismatch")

            event = state.agent.resume_with_human(tool_use_id=tool_use_id, answer=answer)
            return self._to_response(state, event)

    def cleanup(self) -> int:
        return self.store.cleanup(self.session_ttl_seconds)

    @staticmethod
    def _to_response(state, event) -> ChatResponse:
        if event.type == EventType.await_human:
            state.pending_tool_use_id = event.payload.tool_use_id
            return AwaitHumanResponse(
                type="await_human",
                question=event.payload.question,
                tool_use_id=event.payload.tool_use_id,
            )

        state.pending_tool_use_id = None
        return FinalResponse(type="final", answer=event.payload.answer)
