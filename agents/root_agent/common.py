from dotenv import load_dotenv

load_dotenv()

import re
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.lite_llm import LiteLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.tools.tool_context import ToolContext
from google.genai import types

KST = ZoneInfo("Asia/Seoul")

MODEL = LiteLlm(model="ollama_chat/gemma4:31b", think=False)

RESPONSE_RULES = """
# 응답 규칙 (공통)
- 반드시 한국어로만 답한다.
- 내부 추론 과정은 절대 출력하지 않는다. 최종 결론만 1~3문장으로 답한다.
- 정보가 부족하면 무엇이 부족한지 짧게 되묻는다.
- "내일", "이번 주" 등 상대적 시간 표현은 get_current_time을 먼저 호출해 확인한다.
- 사용자가 "저번에", "전에 말했잖아" 등 과거 맥락을 언급하면 load_memory를 먼저 호출한다.
- 다음에도 참고해야 할 중요한 결정/선호/반복 패턴이 생기면 save_memory로 기록한다.
"""

MEMORY_DIR = Path(__file__).parent / "memory" / "sessions"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def load_agent_prompt(agent_dir: Path) -> str:
  soul = (agent_dir / "SOUL.md").read_text(encoding="utf-8")
  skill_path = agent_dir / "SKILL.md"
  skill = ("\n\n" + skill_path.read_text(encoding="utf-8")) if skill_path.exists() else ""
  return soul + skill + RESPONSE_RULES


def save_memory(note: str, tool_context: ToolContext) -> dict:
  """다음 대화에서도 참고해야 할 중요한 정보(사용자 선호, 반복 패턴,
  미해결 요청 등)를 장기 기억으로 저장한다."""
  user_id = tool_context.state.get("user_id", "unknown")
  path = MEMORY_DIR / f"{user_id}.md"
  now = datetime.now(KST).strftime("%Y-%m-%d %H:%M")
  with path.open("a", encoding="utf-8") as f:
    f.write(f"\n## {now}\n{note}\n")
  return {"status": "saved"}


def load_memory(tool_context: ToolContext) -> dict:
  """사용자가 과거 대화/결정을 언급하면 먼저 호출해 이전 기억을 확인한다."""
  user_id = tool_context.state.get("user_id", "unknown")
  path = MEMORY_DIR / f"{user_id}.md"
  content = path.read_text(encoding="utf-8") if path.exists() else "(이전 기록 없음)"
  return {"memory": content}


_LEAK_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bI need to\b",
        r"\bI am the\b",
        r"\bWait,",
        r"\bHowever,",
        r"\bLooking at the\b",
        r"`\w+_agent`",
        r"`\w+` tool",
        r"\bI cannot call\b",
        r"\bI will ask\b",
        r"\bI'll ask\b",
        r"\bSince I don'?t have\b",
        r"\bActually,",
    )
]

_FALLBACK_MESSAGE = "요청 내용을 확인했습니다. 필요한 정보가 있으면 알려주세요."


def _has_korean(text: str) -> bool:
  return bool(re.search(r"[\uac00-\ud7a3]", text))


def _looks_like_leaked_reasoning(text: str) -> bool:
  if not text:
    return False
  hits = sum(1 for pattern in _LEAK_PATTERNS if pattern.search(text))
  if hits >= 2:
    return True
  if hits >= 1 and not _has_korean(text):
    return True
  return len(text) > 200 and not _has_korean(text)


def _extract_korean_sentences(text: str) -> str:
  sentences = re.split(r"(?<=[.!?。])\s+|\n+", text)
  korean = [sentence.strip() for sentence in sentences if _has_korean(sentence.strip())]
  return " ".join(korean)


def sanitize_user_response(text: str) -> str:
  if not _looks_like_leaked_reasoning(text):
    return text
  return _extract_korean_sentences(text) or _FALLBACK_MESSAGE


def strip_leaked_reasoning(
    callback_context: CallbackContext,
    llm_response: LlmResponse,
) -> LlmResponse | None:
  if llm_response.get_function_calls():
    return None
  if not llm_response.content or not llm_response.content.parts:
    return None

  text = "".join(part.text for part in llm_response.content.parts if part.text)
  if not _looks_like_leaked_reasoning(text):
    return None

  cleaned = _extract_korean_sentences(text) or _FALLBACK_MESSAGE
  modified = llm_response.model_copy(deep=True)
  modified.content = types.Content(role="model", parts=[types.Part(text=cleaned)])
  return modified


def get_current_time() -> dict:
  """현재 날짜/시각 반환. 상대적 시간 표현 해석 전 반드시 먼저 호출."""
  now = datetime.now(KST)
  return {
      "date": now.strftime("%Y-%m-%d"),
      "weekday": now.strftime("%A"),
      "time": now.strftime("%H:%M"),
      "tomorrow": (now + timedelta(days=1)).strftime("%Y-%m-%d"),
      "timezone": "Asia/Seoul",
  }
