from google.adk.agents import LlmAgent, SequentialAgent

from ..common import MODEL, read_document, strip_leaked_reasoning
from ..sub_agents.document_agent.tools import draft_report

material_organizer = LlmAgent(
    model=MODEL,
    name="material_organizer",
    description="여러 자료/메모를 읽어 핵심 내용을 정리한다.",
    instruction=(
        "파일이 주어지면 read_document로 읽고, 텍스트로 주어진 내용까지 포함해 "
        "핵심 내용을 문단별로 정리하라."
    ),
    tools=[read_document],
    output_key="organized_material",
    after_model_callback=strip_leaked_reasoning,
)

general_report_drafter = LlmAgent(
    model=MODEL,
    name="general_report_drafter",
    description="정리된 자료로 보고서 초안을 작성한다.",
    instruction=(
        "다음 정리 내용을 바탕으로 draft_report를 호출해 보고서를 작성하라:\n{organized_material}"
    ),
    tools=[draft_report],
    output_key="report_draft",
    after_model_callback=strip_leaked_reasoning,
)

report_reviewer = LlmAgent(
    model=MODEL,
    name="report_reviewer",
    description="작성된 보고서 초안을 검토해 누락/어색한 부분을 고쳐 최종본을 낸다.",
    instruction=(
        "다음 보고서 초안을 검토하라:\n{report_draft}\n\n"
        "논리적 비약, 근거 없는 수치, 어색한 문장이 있으면 고쳐서 최종본을 출력하라. "
        "문제 없으면 그대로 '(검토완료)'를 붙여 출력한다."
    ),
    output_key="final_report",
    after_model_callback=strip_leaked_reasoning,
)

general_report_pipeline = SequentialAgent(
    name="general_report_pipeline",
    description=(
        "여러 자료/메모를 종합해 보고서 초안 작성 후 검토까지 마치는 파이프라인. "
        "출장보고서/주간보고서/기술보고서처럼 자료를 모아 쓰는 일반 보고서 요청에 사용 "
        "(CSV/데이터 분석이 필요한 보고서는 data_report_pipeline 사용)."
    ),
    sub_agents=[material_organizer, general_report_drafter, report_reviewer],
)
