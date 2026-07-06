"""Telegram long polling — webhook/도메인 없이 로컬 테스트 가능."""

from __future__ import annotations

import asyncio
import logging
import os

import httpx
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from gateway.runtime import run_agent_chat

logger = logging.getLogger(__name__)

_bot_app: Application | None = None


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
  final_text = await run_agent_chat(
      user_id,
      session_id,
      update.message.text,
      channel="telegram",
  )
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
