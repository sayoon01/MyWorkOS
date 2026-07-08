_created_keys: set[tuple] = set()


def create_task(title: str, assignee: str | None = None, due_date: str | None = None) -> dict:
  """새 업무를 등록한다. 동일 (title, assignee, due_date) 조합은 중복 등록되지 않는다."""
  key = (title, assignee, due_date)
  if key in _created_keys:
    return {
        "title": title,
        "assignee": assignee or "미배정",
        "due_date": due_date,
        "status": "duplicate_skipped",
    }
  _created_keys.add(key)
  return {"title": title, "assignee": assignee or "미배정", "due_date": due_date, "status": "open"}


def create_tasks_bulk(items: list[dict]) -> dict:
  """여러 업무를 한 번에 일괄 등록한다.
  items 예시: [{"title": "리포트 작성", "assignee": "상아", "due_date": "금요일"}, ...]"""
  created = []
  for item in items:
    created.append({
        "title": item.get("title", "제목 없음"),
        "assignee": item.get("assignee") or "미배정",
        "due_date": item.get("due_date"),
        "status": "open",
    })
  return {"created_count": len(created), "tasks": created}


def list_tasks(assignee: str | None = None, status: str | None = None) -> dict:
  """조건에 맞는 업무 목록을 조회한다."""
  return {"tasks": [], "filter": {"assignee": assignee, "status": status}}


def update_task_status(task_id: str, status: str) -> dict:
  """업무 상태를 변경한다."""
  return {"task_id": task_id, "status": status}
