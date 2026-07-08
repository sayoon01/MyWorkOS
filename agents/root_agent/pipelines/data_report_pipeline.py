from google.adk.agents import LlmAgent, SequentialAgent

from ..common import MODEL, strip_leaked_reasoning
from ..sub_agents.data_agent.tools import export_chart, load_csv, summarize_stats
from ..sub_agents.document_agent.tools import draft_report

data_analyzer = LlmAgent(
    model=MODEL,
    name="data_analyzer",
    description="CSV 파일 또는 텍스트로 제공된 데이터를 분석해 핵심 통계와 특이사항을 요약한다.",
    instruction=(
        "파일 경로가 주어지면 load_csv → summarize_stats 순으로 호출해 분석하라.\n"
        "파일 없이 수치/현황이 텍스트로 주어졌으면 도구 호출 없이 그 내용을 그대로 정리하라.\n"
        "결측치·이상치·특이 추세가 있으면 반드시 언급한다. 요약 텍스트만 출력한다."
    ),
    tools=[load_csv, summarize_stats],
    output_key="analysis_summary",
    after_model_callback=strip_leaked_reasoning,
)

chart_maker = LlmAgent(
    model=MODEL,
    name="chart_maker",
    description="분석 요약에서 시각화가 필요한 지표를 판단해 차트를 생성한다.",
    instruction=(
        "다음 분석 요약을 보고, 시각화가 도움이 될 지표가 있으면 export_chart를 호출하라:\n"
        "{analysis_summary}\n\n시각화가 불필요하면 도구를 호출하지 않고 '시각화 생략'이라고만 출력한다."
    ),
    tools=[export_chart],
    output_key="chart_info",
    after_model_callback=strip_leaked_reasoning,
)

report_writer = LlmAgent(
    model=MODEL,
    name="data_report_writer",
    description="데이터 분석 요약과 차트 정보를 받아 보고서 초안을 작성한다.",
    instruction=(
        "다음 내용을 바탕으로 draft_report를 호출해 보고서 초안을 작성하라.\n"
        "분석 요약:\n{analysis_summary}\n\n차트 정보:\n{chart_info}"
    ),
    tools=[draft_report],
    output_key="final_report",
    after_model_callback=strip_leaked_reasoning,
)

data_report_pipeline = SequentialAgent(
    name="data_report_pipeline",
    description=(
        "데이터(CSV 파일 또는 텍스트 수치)를 분석하고 필요시 차트까지 생성해 보고서로 만드는 파이프라인. "
        "'이 데이터 분석해서 보고서로 만들어줘' 같은 요청에 사용."
    ),
    sub_agents=[data_analyzer, chart_maker, report_writer],
)
