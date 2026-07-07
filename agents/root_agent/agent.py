from google.adk.agents import Agent

from .common import MODEL
from .registry import discover_all_agents

_ALL_AGENTS = discover_all_agents()

# 사람이 관리해야 하는 건 "애매할 때 우선순위" 같은 예외 규칙뿐
_PRIORITY_RULES = """
우선순위 규칙:
- '목차'라는 단어가 포함되면 document_agent가 아니라 반드시 book_agent로 위임한다.
"""


def _build_instruction(agents: list) -> str:
    lines = ["사용자 요청의 성격을 판단해 알맞은 sub_agent에게 위임하라.\n"]
    for a in agents:
        lines.append(f"- {a.description} → {a.name}")
    return "\n".join(lines) + "\n" + _PRIORITY_RULES


root_agent = Agent(
    model=MODEL,
    name="root_agent",
    description="업무·일정·문서·데이터·집필을 조율하는 KETI WorkOS 에이전트",
    instruction=_build_instruction(_ALL_AGENTS),
    sub_agents=_ALL_AGENTS,
)
