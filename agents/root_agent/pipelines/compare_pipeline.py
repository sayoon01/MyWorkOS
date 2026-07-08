from google.adk.agents import LlmAgent, SequentialAgent

from ..common import MODEL, read_document, strip_leaked_reasoning

each_summarizer = LlmAgent(
    model=MODEL,
    name="compare_each_summarizer",
    description="비교 대상 파일들을 각각 읽어 핵심 내용을 요약한다.",
    instruction=(
        "사용자가 제공한 여러 파일 경로 각각에 대해 read_document를 호출하고, "
        "'[파일명] 핵심 내용' 형식으로 파일별 요약을 나열하라."
    ),
    tools=[read_document],
    output_key="individual_summaries",
    after_model_callback=strip_leaked_reasoning,
)

comparator = LlmAgent(
    model=MODEL,
    name="comparator",
    description="여러 문서 요약을 비교해 공통점·차이점·결론을 도출한다.",
    instruction=(
        "다음 문서별 요약을 비교하라:\n{individual_summaries}\n\n"
        "형식:\n[공통점]\n...\n[차이점]\n...\n[결론/추천]\n..."
    ),
    output_key="compare_result",
    after_model_callback=strip_leaked_reasoning,
)

compare_pipeline = SequentialAgent(
    name="compare_pipeline",
    description=(
        "파일 2개 이상을 각각 요약한 뒤 공통점/차이점/결론을 비교하는 파이프라인. "
        "'이 논문 두 개 비교해줘', '제안서 비교해줘' 같은 요청에 사용."
    ),
    sub_agents=[each_summarizer, comparator],
)
