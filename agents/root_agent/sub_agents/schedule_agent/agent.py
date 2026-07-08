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
from .tools import create_calendar_event_notion, create_event, list_events, set_reminder

schedule_agent = Agent(
    model=MODEL,
    name="schedule_agent",
    description="일정·회의·리마인드 관리",
    instruction=load_agent_prompt(Path(__file__).parent),
    tools=[
        get_current_time,
        save_memory,
        load_memory,
        create_event,
        list_events,
        set_reminder,
        create_calendar_event_notion,
    ],
    after_model_callback=strip_leaked_reasoning,
)
