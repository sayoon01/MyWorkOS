import os
import yaml
from pathlib import Path

def load_channels_config() -> dict:
    path = Path(__file__).parent.parent / "config" / "channels.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))["channels"]

def get_token(channel_cfg: dict) -> str:
    token = os.environ.get(channel_cfg["token_env"])
    if not token:
        raise RuntimeError(f"{channel_cfg['token_env']} 환경변수가 없습니다.")
    return token