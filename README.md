# Search Agent

## Run Backend

```bash
uv run uvicorn src.api.app:app --reload --port 8000
```

Health check: `GET http://localhost:8000/health`

## Run Frontend

```bash
cd frontend
npm run dev
```

Frontend default URL: `http://localhost:3000/chat`

Set API base URL if needed:

```bash
export NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Chat API

### `POST /chat/send`

```json
{
  "session_id": "your-session-id",
  "message": "你好"
}
```

### `POST /chat/resume`

```json
{
  "session_id": "your-session-id",
  "tool_use_id": "toolu_xxx",
  "answer": "补充信息"
}
```
