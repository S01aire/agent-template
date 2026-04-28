
"use client";

import { FormEvent, useRef, useState } from "react";

type ChatEvent =
  | { type: "final"; answer: string }
  | { type: "await_human"; question: string; tool_use_id: string };

type Message = {
  role: "user" | "assistant" | "system";
  content: string;
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const SESSION_KEY = "agent_session_id";

function getSessionId() {
  if (typeof window === "undefined") return "";
  const current = window.localStorage.getItem(SESSION_KEY);
  if (current) return current;
  const next = crypto.randomUUID();
  window.localStorage.setItem(SESSION_KEY, next);
  return next;
}

async function postEvent(path: string, body: Record<string, string>) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail ?? "request failed");
  }
  return payload as ChatEvent;
}

export default function ChatPage() {
  const sessionIdRef = useRef("");
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [pendingToolUseId, setPendingToolUseId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "system",
      content: "输入问题开始对话；如果出现追问，直接在输入框回答。",
    },
  ]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    if (!sessionIdRef.current) {
      sessionIdRef.current = getSessionId();
    }
    const sessionId = sessionIdRef.current;

    setInput("");
    setError("");
    setLoading(true);
    setMessages((prev) => [...prev, { role: "user", content: text }]);

    try {
      const data = pendingToolUseId
        ? await postEvent("/chat/resume", {
            session_id: sessionId,
            tool_use_id: pendingToolUseId,
            answer: text,
          })
        : await postEvent("/chat/send", {
            session_id: sessionId,
            message: text,
          });

      if (data.type === "await_human") {
        setPendingToolUseId(data.tool_use_id);
        setMessages((prev) => [
          ...prev,
          { role: "system", content: `追问：${data.question}` },
        ]);
        return;
      }

      setPendingToolUseId(null);
      setMessages((prev) => [...prev, { role: "assistant", content: data.answer }]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="chat-shell">
      <section className="chat-panel">
        <h1 className="chat-title">Search Agent</h1>
        <p className="chat-subtitle">发送第一条消息时会自动创建会话。</p>

        <div className="chat-list">
          {messages.map((message, index) => (
            <article key={`${message.role}-${index}`} className={`msg msg-${message.role}`}>
              {message.content}
            </article>
          ))}
        </div>

        {error ? <p className="chat-error">Error: {error}</p> : null}

        <form className="chat-form" onSubmit={handleSubmit}>
          <input
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={pendingToolUseId ? "请回答追问..." : "请输入问题..."}
            disabled={loading}
          />
          <button className="chat-send" disabled={loading}>
            {loading ? "发送中..." : "发送"}
          </button>
        </form>
      </section>
    </main>
  );
}
