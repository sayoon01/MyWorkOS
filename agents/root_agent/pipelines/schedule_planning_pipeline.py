from google.adk.agents import LlmAgent, SequentialAgent

from ..common import MODEL, get_current_time, strip_leaked_reasoning
from ..sub_agents.schedule_agent.tools import create_calendar_event_notion
from ..sub_agents.task_agent.tools import list_tasks

priority_analyzer = LlmAgent(
    model=MODEL,
    name="priority_analyzer",
    description="업무 목록을 조회해 마감일 기준 우선순위를 분석한다.",
    instruction=(
        "get_current_time으로 오늘 날짜를 확인하고 list_tasks로 업무 목록을 조회하라. "
        "마감일이 임박한 순으로 우선순위를 매겨 정리한다."
    ),
    tools=[get_current_time, list_tasks],
    output_key="prioritized_tasks",
    after_model_callback=strip_leaked_reasoning,
)

schedule_drafter = LlmAgent(
    model=MODEL,
    name="schedule_drafter",
    description="우선순위가 매겨진 업무를 바탕으로 일정표 초안을 만든다.",
    instruction=(
        "다음 우선순위 업무 목록을 바탕으로 날짜별 일정표 초안을 짜라:\n{prioritized_tasks}\n\n"
        "'날짜: 업무명 (예상 소요시간)' 형식으로 출력한다."
    ),
    output_key="schedule_draft",
    after_model_callback=strip_leaked_reasoning,
)

notion_registrar = LlmAgent(
    model=MODEL,
    name="notion_registrar",
    description="일정표 초안을 Notion 캘린더에 등록한다.",
    instruction=(
        "다음 일정표 초안의 각 항목을 create_calendar_event_notion으로 등록하라:\n{schedule_draft}\n\n"
        "등록 후 몇 건 등록됐는지 한국어로 알려준다."
    ),
    tools=[create_calendar_event_notion],
    output_key="notion_result",
    after_model_callback=strip_leaked_reasoning,
)

schedule_planning_pipeline = SequentialAgent(
    name="schedule_planning_pipeline",
    description=(
        "업무 목록을 우선순위로 분석해 일정표 초안을 만들고 Notion 캘린더에 등록하는 파이프라인. "
        "'이번 주 업무 우선순위대로 일정표 짜줘' 같은 요청에 사용."
    ),
    sub_agents=[priority_analyzer, schedule_drafter, notion_registrar],
)
