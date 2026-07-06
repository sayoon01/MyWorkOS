from pathlib import Path

from google.adk.agents import Agent

from ...common import MODEL, get_current_time, load_soul, strip_leaked_reasoning
from .tools import draft_meeting_minutes, draft_report, export_document

document_agent = Agent(
    model=MODEL,
    name="document_agent",
    description="보고서·회의록·문서 작성",
    instruction=load_soul(Path(__file__).parent / "SOUL.md"),
    tools=[get_current_time, draft_meeting_minutes, draft_report, export_document],
    after_model_callback=strip_leaked_reasoning,
)
