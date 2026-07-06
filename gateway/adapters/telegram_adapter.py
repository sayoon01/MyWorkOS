"""Telegram long polling — webhook/도메인 없이 로컬 테스트 가능."""

from __future__ import annotations

import asyncio
import logging
import os

import httpx
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from agents.root_agent.agent import root_agent
from agents.root_agent.common import sanitize_user_response

logger = logging.getLogger(__name__)

APP_NAME = "agentic_runtime"
_bot_app: Application | None = None

session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)


def _agent_debug_enabled() -> bool:
  return os.environ.get("AGENT_DEBUG", "").lower() in ("1", "true", "yes")


async def _ensure_session(user_id: str, session_id: str) -> None:
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


def _debug_log(message: str) -> None:
  if _agent_debug_enabled():
    print(message, flush=True)


async def push_message(chat_id: str, text: str) -> None:
  """heartbeat 등 외부에서 먼저 메시지를 보낼 때 사용."""
  if _bot_app is not None:
    await _bot_app.bot.send_message(chat_id=int(chat_id), text=text)
    return

  token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
  if not token:
    print("[telegram] 봇이 아직 기동되지 않아 push 실패 (TELEGRAM_BOT_TOKEN 없음)", flush=True)
    return

  async with httpx.AsyncClient() as client:
    response = await client.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": int(chat_id), "text": text},
        timeout=30.0,
    )
    if response.is_error:
      print(f"[telegram] push 실패: {response.status_code} {response.text}", flush=True)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  if not update.message or not update.message.text:
    return

  user_id = str(update.effective_user.id)
  session_id = f"tg-{user_id}"
  content = types.Content(role="user", parts=[types.Part(text=update.message.text)])

  _debug_log(f"[gateway] user_id={user_id} ← {update.message.text!r}")

  await _ensure_session(user_id, session_id)

  final_text = ""
  async for event in runner.run_async(
      user_id=user_id,
      session_id=session_id,
      new_message=content,
  ):
    if _agent_debug_enabled():
      author = getattr(event, "author", None)
      if author:
        _debug_log(f"[agent] {author}")
      if event.actions and event.actions.transfer_to_agent:
        _debug_log(f"[transfer] → {event.actions.transfer_to_agent}")
      for fc in event.get_function_calls() or []:
        _debug_log(f"[tool] {fc.name}({fc.args})")
      if event.is_final_response():
        _debug_log("[final] 응답 확정")
    if event.is_final_response() and event.content and event.content.parts:
      final_text = event.content.parts[0].text or ""

  if not final_text:
    final_text = "응답을 생성하지 못했습니다."
  else:
    final_text = sanitize_user_response(final_text)

  await update.message.reply_text(final_text)


async def run_gateway(token: str, *, heartbeat_user_id: str | None = None) -> None:
  """Telegram polling + (선택) heartbeat를 같은 프로세스에서 실행."""
  global _bot_app

  app = Application.builder().token(token).build()
  app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
  _bot_app = app

  async with app:
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    logger.info("Telegram bot polling started")
    print("[gateway] Telegram polling 시작", flush=True)

    if heartbeat_user_id:
      print(f"[gateway] Heartbeat 연동 (user={heartbeat_user_id})", flush=True)
      from heartbeat.scheduler import run_heartbeat

      await run_heartbeat(heartbeat_user_id)
    else:
      await asyncio.Event().wait()


def run_telegram_bot(token: str, *, heartbeat_user_id: str | None = None) -> None:
  asyncio.run(run_gateway(token, heartbeat_user_id=heartbeat_user_id))
