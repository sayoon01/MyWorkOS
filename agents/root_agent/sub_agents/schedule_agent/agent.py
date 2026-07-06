from pathlib import Path

from google.adk.agents import Agent

from ...common import MODEL, get_current_time, load_soul, strip_leaked_reasoning
from .tools import create_event, list_events, set_reminder

schedule_agent = Agent(
    model=MODEL,
    name="schedule_agent",
    description="일정·회의·리마인드 관리",
    instruction=load_soul(Path(__file__).parent / "SOUL.md"),
    tools=[get_current_time, create_event, list_events, set_reminder],
    after_model_callback=strip_leaked_reasoning,
)
