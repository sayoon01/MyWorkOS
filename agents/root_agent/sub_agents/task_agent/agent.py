from pathlib import Path

from google.adk.agents import Agent

from ...common import MODEL, get_current_time, load_soul, strip_leaked_reasoning
from .tools import create_task, list_tasks, update_task_status

task_agent = Agent(
    model=MODEL,
    name="task_agent",
    description="업무 등록·조회·진행상태 관리",
    instruction=load_soul(Path(__file__).parent / "SOUL.md"),
    tools=[get_current_time, create_task, list_tasks, update_task_status],
    after_model_callback=strip_leaked_reasoning,
)
