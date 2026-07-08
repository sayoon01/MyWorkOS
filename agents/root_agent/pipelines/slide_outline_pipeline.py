from google.adk.agents import LlmAgent, SequentialAgent
from ..common import MODEL, strip_leaked_reasoning, read_document

material_reader = LlmAgent(
    model=MODEL,
    name="presentation_material_reader",
    description="발표 자료의 원본 문서를 읽어 장/섹션별 내용을 정리한다.",
    instruction=(
        "파일이 주어지면 read_document로 읽어라. 아니면 제공된 설명을 그대로 사용한다.\n"
        "장/섹션이 구분되면 그 구조를 살려 정리하고, 없으면 주제별로 나눠 정리한다."
    ),
    tools=[read_document],
    output_key="material_by_section",
    after_model_callback=strip_leaked_reasoning,
)

core_message_extractor = LlmAgent(
    model=MODEL,
    name="core_message_extractor",
    description="정리된 자료에서 핵심 메시지를 추출한다.",
    instruction=(
        "다음 자료에서 핵심 메시지 3~5개를 우선순위 순으로 정리하라:\n{material_by_section}\n\n"
        "청중이 가장 궁금해할 결론부터 배치한다."
    ),
    output_key="core_message",
    after_model_callback=strip_leaked_reasoning,
)

slide_structurer = LlmAgent(
    model=MODEL,
    name="slide_structurer",
    description="핵심 메시지를 슬라이드 목차/페이지별 구성으로 짠다.",
    instruction=(
        "다음 핵심 메시지를 바탕으로 슬라이드 구성안을 짜라:\n{core_message}\n\n"
        "'페이지 N: 제목 — 핵심 내용 1줄' 형식으로, 표지·목차·본문·결론 슬라이드를 포함해 출력한다."
    ),
    output_key="slide_outline",
    after_model_callback=strip_leaked_reasoning,
)

script_writer = LlmAgent(
    model=MODEL,
    name="presentation_script_writer",
    description="슬라이드 구성안을 바탕으로 페이지별 발표 멘트를 작성한다.",
    instruction=(
        "다음 슬라이드 구성안의 각 페이지에 대해 30초 분량 발표 멘트를 작성하라:\n{slide_outline}\n\n"
        "'페이지 N 발표 멘트: ...' 형식으로 출력한다."
    ),
    output_key="presentation_script",
    after_model_callback=strip_leaked_reasoning,
)

slide_outline_pipeline = SequentialAgent(
    name="slide_outline_pipeline",
    description=(
        "자료를 읽어 핵심 메시지를 뽑고 슬라이드 목차·페이지 구성·발표 멘트까지 만드는 파이프라인. "
        "'이 자료로 발표자료 만들어줘', 'PPT 목차랑 대본 짜줘' 같은 요청에 사용."
    ),
    sub_agents=[material_reader, core_message_extractor, slide_structurer, script_writer],
)