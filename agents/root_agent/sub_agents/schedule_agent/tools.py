from gateway.adapters.notion_adapter import create_calendar_event_notion


def create_event(
    title: str,
    start_time: str,
    end_time: str,
    attendees: list[str] | None = None,
) -> dict:
  """일정을 등록한다."""
  return {
      "title": title,
      "start_time": start_time,
      "end_time": end_time,
      "attendees": attendees or [],
      "conflict": False,
  }


def list_events(date: str) -> dict:
  """특정 날짜의 일정을 조회한다."""
  return {"date": date, "events": []}


def set_reminder(event_id: str, remind_at: str) -> dict:
  """리마인드를 설정한다."""
  return {"event_id": event_id, "remind_at": remind_at}
