from google.adk.agents import LlmAgent, SequentialAgent

from ..common import MODEL, read_document, strip_leaked_reasoning

doc_reader = LlmAgent(
    model=MODEL,
    name="quick_doc_reader",
    description="파일을 읽어 원문 내용을 확보한다.",
    instruction="read_document로 파일을 읽는다. 읽은 내용을 그대로 출력한다 (요약하지 않는다).",
    tools=[read_document],
    output_key="raw_content",
    after_model_callback=strip_leaked_reasoning,
)

quick_summarizer = LlmAgent(
    model=MODEL,
    name="quick_summarizer",
    description="문서 내용을 3줄 요약 + 핵심 키워드로 압축한다.",
    instruction=(
        "다음 문서 내용을 3줄 이내로 요약하고 핵심 키워드 5개를 뽑아라:\n{raw_content}\n\n"
        "형식:\n[3줄 요약]\n...\n[핵심 키워드]\n..."
    ),
    output_key="document_summary",
    after_model_callback=strip_leaked_reasoning,
)

quick_insight_pipeline = SequentialAgent(
    name="quick_insight_pipeline",
    description=(
        "문서를 빠르게 읽어 3줄 요약과 핵심 키워드만 뽑아주는 파이프라인. "
        "'이 문서 뭐하는 거야', '핵심만 알려줘' 같은 요청에 사용."
    ),
    sub_agents=[doc_reader, quick_summarizer],
)
