"""All gateway adapters share one session_service + runner."""

from __future__ import annotations

import os
import time

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.root_agent.agent import root_agent
from agents.root_agent.common import sanitize_user_response

APP_NAME = "agentic_runtime"

session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)


def agent_debug_enabled() -> bool:
  return os.environ.get("AGENT_DEBUG", "").lower() in ("1", "true", "yes")


def debug_log(message: str) -> None:
  if agent_debug_enabled():
    print(message, flush=True)


async def ensure_session(user_id: str, session_id: str) -> None:
  session = await session_service.get_session(
      app_name=APP_NAME,
      user_id=user_id,
      session_id=session_id,
  )
  if session is None:
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
        state={"user_id": user_id},
    )


async def run_agent_chat(
    user_id: str,
    session_id: str,
    message: str,
    *,
    channel: str = "gateway",
) -> str:
  await ensure_session(user_id, session_id)
  debug_log(f"[{channel}] user_id={user_id} ← {message!r}")

  content = types.Content(role="user", parts=[types.Part(text=message)])
  final_text = ""
  start = time.monotonic()
  async for event in runner.run_async(
      user_id=user_id,
      session_id=session_id,
      new_message=content,
  ):
    elapsed = time.monotonic() - start
    if agent_debug_enabled():
      author = getattr(event, "author", None)
      if author:
        debug_log(f"[agent] {author}  (+{elapsed:.1f}s)")
      if event.actions and event.actions.transfer_to_agent:
        debug_log(f"[transfer] → {event.actions.transfer_to_agent}  (+{elapsed:.1f}s)")
      for fc in event.get_function_calls() or []:
        debug_log(f"[tool] {fc.name}({fc.args})  (+{elapsed:.1f}s)")
      if event.is_final_response():
        debug_log(f"[final] 응답 확정  (+{elapsed:.1f}s)")
    if event.is_final_response() and event.content and event.content.parts:
      final_text = event.content.parts[0].text or ""

  if not final_text:
    return "응답을 생성하지 못했습니다."
  return sanitize_user_response(final_text)
