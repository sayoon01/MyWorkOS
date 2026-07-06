from dotenv import load_dotenv

load_dotenv()

import asyncio
import os

from .auth import get_token, load_channels_config
from .adapters.telegram_adapter import run_gateway
from .adapters.web_adapter import run_web_server


def _agent_debug_enabled() -> bool:
    return os.environ.get("AGENT_DEBUG", "").lower() in ("1", "true", "yes")


def _heartbeat_enabled() -> bool:
    return os.environ.get("HEARTBEAT_ENABLED", "1").lower() in ("1", "true", "yes")


async def main_async() -> None:
    channels = load_channels_config()
    tasks: list[asyncio.Task] = []

    if channels.get("web", {}).get("enabled"):
        port = int(channels["web"].get("port", os.environ.get("WEBHOOK_PORT", 8080)))
        print(f"[gateway] Web 채널 기동 (port={port})", flush=True)
        tasks.append(asyncio.create_task(run_web_server(port)))

    if channels.get("telegram", {}).get("enabled"):
        token = get_token(channels["telegram"])
        heartbeat_user_id = None
        if _heartbeat_enabled():
            heartbeat_user_id = os.environ.get("HEARTBEAT_TARGET_USER_ID", "").strip() or None

        print("[gateway] Telegram 채널 기동", flush=True)
        if heartbeat_user_id:
            print("[gateway] Heartbeat + Telegram 통합 모드", flush=True)
        if _agent_debug_enabled():
            print(
                "[gateway] AGENT_DEBUG=on — 메시지마다 "
                "[agent]/[transfer]/[tool] 로그가 이 터미널에 출력됩니다.",
                flush=True,
            )
        tasks.append(asyncio.create_task(run_gateway(token, heartbeat_user_id=heartbeat_user_id)))

    if not tasks:
        raise SystemExit("channels.yaml에 enabled 채널이 없습니다.")

    await asyncio.gather(*tasks)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
