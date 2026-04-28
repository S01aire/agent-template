from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from threading import RLock
from typing import Callable

from src.agent.base import BaseAgent


@dataclass(slots=True)
class SessionState:
    agent: BaseAgent
    messages: list[dict] = field(default_factory=list)
    pending_tool_use_id: str | None = None
    updated_at: datetime = field(default_factory=datetime.utcnow)
    lock: RLock = field(default_factory=RLock)

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()


class MemorySessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, SessionState] = {}
        self._lock = RLock()

    def get_or_create(self, session_id: str, factory: Callable[[], BaseAgent]) -> SessionState:
        with self._lock:
            state = self._sessions.get(session_id)
            if state is None:
                state = SessionState(agent=factory())
                self._sessions[session_id] = state
            state.touch()
            return state

    def get(self, session_id: str) -> SessionState | None:
        with self._lock:
            state = self._sessions.get(session_id)
            if state is not None:
                state.touch()
            return state

    def cleanup(self, ttl_seconds: int) -> int:
        cutoff = datetime.utcnow() - timedelta(seconds=ttl_seconds)
        removed = 0
        with self._lock:
            for session_id in list(self._sessions.keys()):
                if self._sessions[session_id].updated_at < cutoff:
                    del self._sessions[session_id]
                    removed += 1
        return removed
