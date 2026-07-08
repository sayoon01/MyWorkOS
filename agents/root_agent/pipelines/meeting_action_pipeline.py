from google.adk.agents import LlmAgent, SequentialAgent
from ..common import MODEL, strip_leaked_reasoning, get_current_time
from ..sub_agents.document_agent.tools import draft_meeting_minutes
from ..sub_agents.task_agent.tools import create_tasks_bulk

# ── Step 1: 이해/요약 — 원본 메모를 회의록으로 정리 ──
minutes_writer = LlmAgent(
    model=MODEL,
    name="minutes_writer",
    description="원본 회의 메모를 정식 회의록으로 정리한다.",
    instruction=(
        "사용자가 제공한 회의 메모/녹취 내용으로 draft_meeting_minutes를 호출해 회의록을 작성한다.\n"
        "발언 내용을 각색하지 않고 사실만 정리한다. 회의록 본문만 출력한다."
    ),
    tools=[draft_meeting_minutes],
    output_key="meeting_minutes",
    after_model_callback=strip_leaked_reasoning,
)

# ── Step 2: 구조화 — 회의록에서 액션아이템 추출 ──
action_extractor = LlmAgent(
    model=MODEL,
    name="action_extractor",
    description="회의록에서 실행할 업무(액션아이템)를 추출한다.",
    instruction=(
        "다음 회의록에서 실제로 수행해야 할 업무를 찾아 목록화하라:\n{meeting_minutes}\n\n"
        "각 항목을 '제목 | 담당자(불명확하면 미배정) | 마감일(불명확하면 없음)' 형식으로 한 줄씩 출력한다.\n"
        "실행할 업무가 없으면 '추출된 액션아이템 없음'이라고만 출력한다."
    ),
    output_key="action_items",
    after_model_callback=strip_leaked_reasoning,
)

# ── Step 3: 산출물 생성 — 액션아이템을 실제 업무로 등록 ──
task_registrar = LlmAgent(
    model=MODEL,
    name="task_registrar",
    description="추출된 액션아이템을 실제 업무로 일괄 등록한다.",
    instruction=(
        "다음 액션아이템 목록을 파싱해서 create_tasks_bulk를 **정확히 1번만** 호출하라:\n"
        "{action_items}\n\n"
        "'추출된 액션아이템 없음'이면 도구를 호출하지 않고 그대로 안내한다.\n"
        "등록이 끝나면 몇 건이 등록됐는지 한국어로 알려준다."
    ),
    tools=[get_current_time, create_tasks_bulk],
    output_key="registration_result",
    after_model_callback=strip_leaked_reasoning,
)

meeting_action_pipeline = SequentialAgent(
    name="meeting_action_pipeline",
    description=(
        "회의 메모/녹취를 받아 회의록 작성 → 액션아이템 추출 → 업무 자동 등록까지 "
        "한 번에 처리하는 파이프라인. '회의 내용 정리하고 할 일 등록해줘', "
        "'이 메모에서 액션아이템 뽑아서 업무로 만들어줘' 같은 요청에 사용."
    ),
    sub_agents=[minutes_writer, action_extractor, task_registrar],
)