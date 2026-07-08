from google.adk.agents import LlmAgent, SequentialAgent
from ..common import MODEL, strip_leaked_reasoning, read_document

problem_finder = LlmAgent(
    model=MODEL,
    name="problem_finder",
    description="자료(문서/코드/데이터 설명)에서 문제점과 개선 여지를 찾는다.",
    instruction=(
        "파일이 주어지면 read_document로 읽고, 아니면 제공된 설명을 바탕으로 "
        "문제점·부족한 점·리스크를 목록화하라. 근거 없는 지적은 하지 않는다."
    ),
    tools=[read_document],
    output_key="problem_summary",
    after_model_callback=strip_leaked_reasoning,
)

recommender = LlmAgent(
    model=MODEL,
    name="recommender",
    description="발견된 문제점에 대한 개선안을 우선순위와 함께 제시한다.",
    instruction=(
        "다음 문제점을 바탕으로 개선안을 제시하라:\n{problem_summary}\n\n"
        "각 개선안에 우선순위(상/중/하)와 이유를 함께 표시한다."
    ),
    output_key="recommendation",
    after_model_callback=strip_leaked_reasoning,
)

recommendation_pipeline = SequentialAgent(
    name="recommendation_pipeline",
    description=(
        "자료의 문제점을 찾고 우선순위가 매겨진 개선안까지 제시하는 파이프라인. "
        "'이 PPT 어떻게 고치지', '이 코드 리팩토링 방향' 같은 요청에 사용."
    ),
    sub_agents=[problem_finder, recommender],
)