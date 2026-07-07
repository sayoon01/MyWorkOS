# agents/root_agent/pipelines/data_report_pipeline.py
from google.adk.agents import LlmAgent, SequentialAgent
from ..common import MODEL, strip_leaked_reasoning
from ..sub_agents.data_agent.tools import load_csv, summarize_stats
from ..sub_agents.document_agent.tools import draft_report

# Step 1: 이해/요약 — 데이터 로드 + 통계 계산
data_analyzer = LlmAgent(
    model=MODEL,
    name="data_analyzer",
    description="CSV를 분석해 핵심 통계와 특이사항을 요약한다.",
    instruction=(
        "load_csv로 파일을 확인하고, summarize_stats로 숫자형 컬럼 통계를 계산하라.\n"
        "결측치·이상치가 있으면 반드시 언급한다. 분석 결과를 요약 텍스트로만 출력한다."
    ),
    tools=[load_csv, summarize_stats],
    output_key="analysis_summary",
    after_model_callback=strip_leaked_reasoning,
)

# Step 2: 산출물 생성 — 분석 결과를 보고서로
report_writer = LlmAgent(
    model=MODEL,
    name="data_report_writer",
    description="데이터 분석 요약을 받아 보고서 초안을 작성한다.",
    instruction=(
        "다음 분석 결과를 바탕으로 draft_report를 호출해 보고서 초안을 작성하라:\n{analysis_summary}\n\n"
        "결측치·이상치 언급이 있으면 보고서에도 그대로 반영한다."
    ),
    tools=[draft_report],
    output_key="final_report",
    after_model_callback=strip_leaked_reasoning,
)

data_report_pipeline = SequentialAgent(
    name="data_report_pipeline",
    description=(
        "CSV 분석 → 보고서 작성을 자동으로 이어 처리하는 파이프라인. "
        "'이 데이터 분석해서 보고서로 만들어줘' 같은 요청에 사용."
    ),
    sub_agents=[data_analyzer, report_writer],
)