from dotenv import load_dotenv

load_dotenv()

import os

from .auth import load_channels_config, get_token
from .adapters.telegram_adapter import run_telegram_bot
# from .adapters.slack_adapter import run_slack_bot   # 보류
# from .adapters.teams_adapter import run_teams_bot    # 보류


def _agent_debug_enabled() -> bool:
    return os.environ.get("AGENT_DEBUG", "").lower() in ("1", "true", "yes")


def main():
    channels = load_channels_config()

    if channels.get("telegram", {}).get("enabled"):
        token = get_token(channels["telegram"])
        print("[gateway] Telegram 채널 기동", flush=True)
        if _agent_debug_enabled():
            print(
                "[gateway] AGENT_DEBUG=on — Telegram 메시지마다 "
                "[agent]/[transfer]/[tool] 로그가 이 터미널에 출력됩니다.",
                flush=True,
            )
        run_telegram_bot(token)  # blocking polling

    # Phase 2에서 슬랙/팀즈 켤 때 asyncio.gather로 동시 기동하도록 변경 예정

if __name__ == "__main__":
    main()