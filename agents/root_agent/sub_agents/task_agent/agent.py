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
from .tools import create_task, list_tasks, update_task_status

task_agent = Agent(
    model=MODEL,
    name="task_agent",
    description="업무 등록·조회·진행상태 관리",
    instruction=load_agent_prompt(Path(__file__).parent),
    tools=[
        get_current_time,
        save_memory,
        load_memory,
        create_task,
        list_tasks,
        update_task_status,
    ],
    after_model_callback=strip_leaked_reasoning,
)
