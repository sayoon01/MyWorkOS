from google.adk.agents import LlmAgent, SequentialAgent

from ..common import MODEL, get_current_time, strip_leaked_reasoning
from ..sub_agents.task_agent.tools import create_tasks_bulk

requirement_analyzer = LlmAgent(
    model=MODEL,
    name="requirement_analyzer",
    description="프로젝트/업무 요청을 분석해 필요한 작업들을 정리한다.",
    instruction=(
        "사용자의 요청을 분석해 필요한 작업들을 실행 순서대로 나열하라. "
        "각 작업의 목적도 한 줄씩 붙인다."
    ),
    output_key="requirements_summary",
    after_model_callback=strip_leaked_reasoning,
)

plan_builder = LlmAgent(
    model=MODEL,
    name="execution_plan_builder",
    description="정리된 작업들을 우선순위/순서가 있는 실행계획으로 구조화한다.",
    instruction=(
        "다음 작업 목록을 바탕으로 실행계획을 짜라:\n{requirements_summary}\n\n"
        "'단계 N: 작업명 — 예상 산출물' 형식으로 출력한다."
    ),
    output_key="execution_plan",
    after_model_callback=strip_leaked_reasoning,
)

plan_registrar = LlmAgent(
    model=MODEL,
    name="plan_registrar",
    description="실행계획의 각 단계를 실제 업무로 일괄 등록한다.",
    instruction=(
        "다음 실행계획을 파싱해서 create_tasks_bulk를 **정확히 1번만** 호출하라:\n"
        "{execution_plan}\n\n"
        "등록 후 몇 건 등록됐는지 한국어로 알려준다."
    ),
    tools=[get_current_time, create_tasks_bulk],
    output_key="registration_result",
    after_model_callback=strip_leaked_reasoning,
)

requirement_plan_pipeline = SequentialAgent(
    name="requirement_plan_pipeline",
    description=(
        "프로젝트/업무 요청을 분석해 실행계획을 짜고 각 단계를 업무로 자동 등록하는 파이프라인. "
        "'이 프로젝트 뭐부터 해야 돼' 같은 요청에 사용."
    ),
    sub_agents=[requirement_analyzer, plan_builder, plan_registrar],
)
