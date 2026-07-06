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
from .tools import consistency_checker_tool, export_tool, outline_tool

book_agent = Agent(
    model=MODEL,
    name="book_agent",
    description=(
        "책/기술문서 생성 — 목차(outline) 구성, 여러 챕터/섹션으로 이루어진 "
        "장문 문서 작성 시 사용. '목차', '구조를 짜줘' 같은 요청은 반드시 여기로"
    ),
    instruction=load_agent_prompt(Path(__file__).parent),
    tools=[
        get_current_time,
        save_memory,
        load_memory,
        outline_tool,
        consistency_checker_tool,
        export_tool,
    ],
    after_model_callback=strip_leaked_reasoning,
)
