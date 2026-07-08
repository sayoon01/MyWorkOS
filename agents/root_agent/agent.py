from google.adk.agents import Agent

from .common import MODEL
from .registry import discover_all_agents

_ALL_AGENTS = discover_all_agents()

# 사람이 관리해야 하는 건 "애매할 때 우선순위" 같은 예외 규칙뿐
_PRIORITY_RULES = """
우선순위 규칙:
- '목차'가 슬라이드/PPT/발표 맥락이면 slide_outline_pipeline, 책/챕터별 업무분배 맥락이면 book_task_pipeline,
  그 외 단순 문서 목차는 book_agent로 위임한다.
- 여러 파일을 "비교"해달라는 요청은 compare_pipeline, 파일 하나만 "요약/이해"는 quick_insight_pipeline으로 위임한다.
- CSV/엑셀 기반 분석+보고서는 data_report_pipeline, 자료/메모 종합형 보고서는 general_report_pipeline으로 위임한다.
- '회의'가 언급돼도, 사용자가 실제 회의 내용/메모/발언을 함께 제공하며 "정리해서 할 일 등록"까지 요청한 경우에만
  meeting_action_pipeline으로 위임한다. 단순히 이전 회의 일정을 묻거나 확인하는 요청(예: "그 회의 언제야",
  "다시 확인해줘")은 반드시 schedule_agent로 위임한다.
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
