from pathlib import Path

from google.adk.agents import Agent

from ...common import (
    MODEL,
    get_current_time,
    load_agent_prompt,
    load_memory,
    save_memory,
    strip_leaked_reasoning,
)
from .tools import export_chart, load_csv, summarize_stats

data_agent = Agent(
    model=MODEL,
    name="data_agent",
    description="엑셀·CSV 데이터 분석",
    instruction=load_agent_prompt(Path(__file__).parent),
    tools=[
        get_current_time,
        save_memory,
        load_memory,
        load_csv,
        summarize_stats,
        export_chart,
    ],
    after_model_callback=strip_leaked_reasoning,
)
