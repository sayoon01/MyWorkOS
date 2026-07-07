"""Web chat channel — telegram과 동일한 session_service/runner 공유."""

from __future__ import annotations

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from gateway.runtime import run_agent_chat

app = FastAPI()


class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    session_id = f"user-{req.user_id}"
    reply = await run_agent_chat(req.user_id, session_id, req.message, channel="web")
    return ChatResponse(reply=reply)


async def run_web_server(port: int) -> None:
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    print(f"[web] FastAPI 서버 시작 — http://0.0.0.0:{port}/chat", flush=True)
    await server.serve()