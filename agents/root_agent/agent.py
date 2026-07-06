from google.adk.agents import Agent

from .common import MODEL
from .sub_agents.book_agent.agent import book_agent
from .sub_agents.data_agent.agent import data_agent
from .sub_agents.document_agent.agent import document_agent
from .sub_agents.schedule_agent.agent import schedule_agent
from .sub_agents.task_agent.agent import task_agent

root_agent = Agent(
    model=MODEL,
    name="root_agent",
    description="업무·일정·문서·데이터·집필을 조율하는 KETI WorkOS 에이전트",
    instruction=(
        "사용자 요청의 성격을 판단해 알맞은 sub_agent에게 위임하라.\n"
        "- 업무 등록/조회 → task_agent\n"
        "- 일정/회의/리마인드 → schedule_agent\n"
        "- 보고서/회의록 작성 → document_agent\n"
        "- 엑셀/CSV 분석 → data_agent\n"
        "- 책/기술문서·목차 생성 → book_agent"
    ),
    sub_agents=[task_agent, schedule_agent, document_agent, data_agent, book_agent],
)
