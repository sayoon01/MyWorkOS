from pathlib import Path

from google.adk.agents import Agent

from ...common import MODEL, get_current_time, load_soul, strip_leaked_reasoning
from .tools import consistency_checker_tool, export_tool, outline_tool

book_agent = Agent(
    model=MODEL,
    name="book_agent",
    description="책/기술문서 생성",
    instruction=load_soul(Path(__file__).parent / "SOUL.md"),
    tools=[get_current_time, outline_tool, consistency_checker_tool, export_tool],
    after_model_callback=strip_leaked_reasoning,
)
