"""FastAPI web chat channel — Telegram과 동급 HTTP 엔드포인트."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from gateway.runtime import run_agent_chat

router = FastAPI(title="KETI WorkOS Web Gateway")


class ChatRequest(BaseModel):
  user_id: str
  message: str


@router.post("/chat")
async def chat(req: ChatRequest) -> dict[str, str]:
  session_id = f"web-{req.user_id}"
  reply = await run_agent_chat(
      req.user_id,
      session_id,
      req.message,
      channel="web",
  )
  return {"reply": reply}


async def run_web_server(port: int) -> None:
  import uvicorn

  config = uvicorn.Config(router, host="0.0.0.0", port=port, log_level="info")
  server = uvicorn.Server(config)
  await server.serve()
