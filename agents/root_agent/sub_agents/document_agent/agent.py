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
from .tools import draft_meeting_minutes, draft_report, export_document

document_agent = Agent(
    model=MODEL,
    name="document_agent",
    description=(
        "단건 보고서/회의록 작성 — 이미 정해진 형식의 짧은 문서. "
        "목차·챕터 구성이 필요없는 경우"
    ),
    instruction=load_agent_prompt(Path(__file__).parent),
    tools=[
        get_current_time,
        save_memory,
        load_memory,
        draft_meeting_minutes,
        draft_report,
        export_document,
    ],
    after_model_callback=strip_leaked_reasoning,
)
