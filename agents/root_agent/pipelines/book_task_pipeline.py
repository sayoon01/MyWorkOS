from google.adk.agents import LlmAgent, SequentialAgent
from ..common import MODEL, strip_leaked_reasoning
from ..sub_agents.book_agent.tools import outline_tool
from ..sub_agents.task_agent.tools import create_tasks_bulk

outline_planner = LlmAgent(
    model=MODEL,
    name="outline_planner",
    description="문서/기술문서 목차를 생성한다.",
    instruction=(
        "outline_tool로 목차를 생성하고, 각 챕터명을 한 줄씩 텍스트로 출력하라. "
        "doc_type이 불명확하면 'general'로 간주한다."
    ),
    tools=[outline_tool],
    output_key="book_outline",
    after_model_callback=strip_leaked_reasoning,
)

chapter_task_registrar = LlmAgent(
    model=MODEL,
    name="chapter_task_registrar",
    description="문서 목차의 각 챕터를 집필 업무로 일괄 등록한다.",
    instruction=(
        "다음은 문서 목차이다:\n{book_outline}\n\n"
        "각 챕터명 뒤에 '집필'이라는 단어를 붙여 업무 제목으로 만들고, "
        "create_tasks_bulk를 **정확히 1번만** 호출해 모두 등록하라.\n"
        "등록 완료 후 몇 개 챕터가 등록됐는지 한국어로 알려준다."
    ),
    tools=[create_tasks_bulk],
    output_key="registration_result",
    after_model_callback=strip_leaked_reasoning,
)

book_task_pipeline = SequentialAgent(
    name="book_task_pipeline",
    description=(
        "장문 문서/기술문서의 목차를 만들고, 각 챕터를 집필 업무로 자동 등록하는 파이프라인. "
        "'이 문서 목차 짜고 챕터별로 할 일 나눠줘' 같은 요청에 사용."
    ),
    sub_agents=[outline_planner, chapter_task_registrar],
)