"""KETI WorkOS 에이전트 스모크 테스트.

root_agent → sub_agent 라우팅과 응답 품질(영어 추론 노출)을 검증한다.
실행: python test/smoke_test.py
"""

from __future__ import annotations

import asyncio
import sys

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.root_agent.agent import root_agent
from agents.root_agent.common import _looks_like_leaked_reasoning, sanitize_user_response

APP_NAME = "agentic_runtime"

CASES = [
    #("내일 오후 3시 회의 잡아줘", "schedule_agent"),
    ("이번 주 업무 목록 보여줘", "task_agent"),
    ("어제 회의록 초안 써줘", "document_agent"),
    ("이 CSV 요약해줘", "data_agent"),
    ("보고서 목차 하나 짜줘", "book_agent"),
    ("어제 얘기한 회의 다시 확인해줘", "schedule_agent"),
    ("다음부터 회의는 항상 오후 2시 이후로만 잡아줘", "schedule_agent"),
    (
    "오늘 회의 메모야: 상아가 데이터 분석 리포트 다음주 금요일까지 작성, "
    "민수가 API 문서 이번주 안에 정리. 이거 회의록으로 정리하고 할 일로 등록해줘",
    "meeting_action_pipeline"
)
]


async def run_case(
    runner: Runner,
    session_service: InMemorySessionService,
    index: int,
    text: str,
    expected_agent: str,
) -> tuple[bool, bool]:
  user_id = "smoke-user"
  session_id = f"smoke-{index}-{expected_agent}"
  await session_service.create_session(
      app_name=APP_NAME,
      user_id=user_id,
      session_id=session_id,
      state={"user_id": user_id},
  )
  content = types.Content(role="user", parts=[types.Part(text=text)])

  routed_to: str | None = None
  tools_called: list[str] = []
  final_text = ""

  async for event in runner.run_async(
      user_id=user_id,
      session_id=session_id,
      new_message=content,
  ):
    if event.actions and event.actions.transfer_to_agent:
      routed_to = event.actions.transfer_to_agent
    for fc in event.get_function_calls() or []:
      tools_called.append(fc.name)
    if event.is_final_response() and event.content and event.content.parts:
      final_text = event.content.parts[0].text or ""

  route_ok = routed_to == expected_agent
  leaked = _looks_like_leaked_reasoning(final_text)
  clean_ok = not leaked
  display_text = sanitize_user_response(final_text)

  print(f"\n[{text}]")
  print(f"  기대: {expected_agent}")
  print(f"  라우팅: {'✅' if route_ok else '❌'} (got {routed_to})")
  print(f"  도구호출: {tools_called}")
  print(f"  응답품질: {'❌ 영어 추론 노출' if leaked else '✅'}")
  print(f"  응답: {display_text[:120]}")

  return route_ok, clean_ok


async def main() -> int:
  print("=== KETI WorkOS smoke test ===")
  print("root_agent sub_agents:", [a.name for a in root_agent.sub_agents])

  session_service = InMemorySessionService()
  runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

  route_pass = clean_pass = 0
  for i, (text, expected) in enumerate(CASES):
    route_ok, clean_ok = await run_case(runner, session_service, i, text, expected)
    route_pass += int(route_ok)
    clean_pass += int(clean_ok)

  total = len(CASES)
  print(f"\n=== 결과: 라우팅 {route_pass}/{total}, 응답품질 {clean_pass}/{total} ===")

  if route_pass == total and clean_pass == total:
    return 0
  return 1


if __name__ == "__main__":
  sys.exit(asyncio.run(main()))
