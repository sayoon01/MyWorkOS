"""asyncio 폴링 기반 heartbeat — 파일 감지 · 아침 브리핑."""

from __future__ import annotations

import asyncio
import os
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

KST = ZoneInfo("Asia/Seoul")
UPLOAD_DIR = Path(os.environ.get("HEARTBEAT_UPLOAD_DIR", "data/uploads"))
CHECK_INTERVAL_SEC = int(os.environ.get("HEARTBEAT_CHECK_INTERVAL_SEC", "300"))

_seen_files: set[str] = set()


async def notify_via_bot(user_id: str, text: str) -> str:
  """heartbeat가 감지한 걸 에이전트에게 대신 물어보게 하는 헬퍼."""
  from gateway.adapters.telegram_adapter import push_message
  from gateway.runtime import run_agent_chat

  session_id = f"user-{user_id}"
  final_text = await run_agent_chat(user_id, session_id, text, channel="heartbeat")
  print(f"[heartbeat] {final_text}", flush=True)
  await push_message(chat_id=user_id, text=final_text)
  return final_text


async def check_new_files(target_user_id: str) -> None:
  if not UPLOAD_DIR.exists():
    print(f"[heartbeat] 업로드 디렉터리가 없습니다: {UPLOAD_DIR.resolve()}", flush=True)
    return

  current = {f.name for f in UPLOAD_DIR.glob("*.csv")}
  new_files = current - _seen_files
  _seen_files.update(current)
  for name in new_files:
    print(f"[heartbeat] 신규 파일 감지: {name}", flush=True)
    await notify_via_bot(
        target_user_id,
        f"{UPLOAD_DIR / name} 파일이 새로 들어왔어. 요약해줘.",
    )


async def daily_briefing(target_user_id: str) -> None:
  print("[heartbeat] 아침 브리핑 시작", flush=True)
  await notify_via_bot(target_user_id, "오늘 마감인 업무 있는지 확인해줘.")


async def run_heartbeat(target_user_id: str) -> None:
  if UPLOAD_DIR.exists():
    initial = {f.name for f in UPLOAD_DIR.glob("*.csv")}
    _seen_files.update(initial)
    print(
        f"[heartbeat] 업로드 디렉터리 초기 스캔: {len(initial)}개 CSV (기존 파일은 무시)",
        flush=True,
    )
  else:
    print(f"[heartbeat] 업로드 디렉터리가 없습니다: {UPLOAD_DIR.resolve()}", flush=True)

  print(
      f"[heartbeat] 감시 시작 — {UPLOAD_DIR.resolve()} / {CHECK_INTERVAL_SEC}초 간격",
      flush=True,
  )

  last_briefing_date: date | None = None
  while True:
    await check_new_files(target_user_id)

    now = datetime.now(KST)
    if now.hour == 9 and last_briefing_date != now.date():
      await daily_briefing(target_user_id)
      last_briefing_date = now.date()

    await asyncio.sleep(CHECK_INTERVAL_SEC)


def main() -> None:
  target_user_id = os.environ.get("HEARTBEAT_TARGET_USER_ID", "").strip()
  if not target_user_id:
    raise SystemExit(
        "HEARTBEAT_TARGET_USER_ID 환경변수가 필요합니다. "
        "(Telegram numeric user id — @userinfobot으로 확인)"
    )
  asyncio.run(run_heartbeat(target_user_id=target_user_id))


if __name__ == "__main__":
  main()
