from google.adk.agents import LlmAgent, SequentialAgent
from ..common import MODEL, strip_leaked_reasoning, read_document

context_retriever = LlmAgent(
    model=MODEL,
    name="context_retriever",
    description="문서에서 질문과 관련된 부분을 찾아 근거로 추출한다.",
    instruction=(
        "read_document로 파일을 읽고, 사용자 질문과 관련된 부분만 발췌하라. "
        "관련 없는 내용은 버린다. 발췌 내용과 위치(섹션/문단 등)를 함께 출력한다."
    ),
    tools=[read_document],
    output_key="retrieved_context",
    after_model_callback=strip_leaked_reasoning,
)

qa_answerer = LlmAgent(
    model=MODEL,
    name="qa_answerer",
    description="추출된 근거를 바탕으로 질문에 답한다.",
    instruction=(
        "다음 발췌 내용을 근거로 사용자 질문에 답하라:\n{retrieved_context}\n\n"
        "근거에 없는 내용은 추측하지 않고 '문서에서 확인 불가'라고 답한다."
    ),
    output_key="answer",
    after_model_callback=strip_leaked_reasoning,
)

qa_pipeline = SequentialAgent(
    name="qa_pipeline",
    description=(
        "문서에서 질문과 관련된 부분을 찾아 근거 기반으로 답하는 파이프라인. "
        "'이 계약서에 위약금 있어?', 'ALD 온도는 몇 도야?' 같은 문서 기반 질문에 사용."
    ),
    sub_agents=[context_retriever, qa_answerer],
)