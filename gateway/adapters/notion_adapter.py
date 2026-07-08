"""Notion 데이터베이스에 일정을 등록하는 아웃바운드 연동."""

import os

from notion_client import Client

_client: Client | None = None


def _get_client() -> Client:
  global _client
  if _client is None:
    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
      raise RuntimeError("NOTION_TOKEN 환경변수가 필요합니다.")
    _client = Client(auth=token)
  return _client


def create_calendar_event_notion(title: str, date: str, memo: str = "") -> dict:
  """Notion 캘린더 데이터베이스에 일정을 등록한다.
  date는 YYYY-MM-DD 형식이어야 한다."""
  database_id = os.environ.get("NOTION_CALENDAR_DB_ID", "").strip()
  if not database_id:
    return {"error": "NOTION_CALENDAR_DB_ID 환경변수가 필요합니다."}
  try:
    client = _get_client()
    page = client.pages.create(
        parent={"database_id": database_id},
        properties={
            "이름": {"title": [{"text": {"content": title}}]},
            "날짜": {"date": {"start": date}},
            "메모": {"rich_text": [{"text": {"content": memo}}]},
        },
    )
    return {"status": "created", "notion_page_id": page["id"]}
  except Exception as e:
    return {"error": f"Notion 등록 실패: {e}"}
