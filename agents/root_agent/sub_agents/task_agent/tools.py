def create_task(title: str, assignee: str | None = None, due_date: str | None = None) -> dict:
  """새 업무를 등록한다."""
  return {"title": title, "assignee": assignee or "미배정", "due_date": due_date, "status": "open"}


def list_tasks(assignee: str | None = None, status: str | None = None) -> dict:
  """조건에 맞는 업무 목록을 조회한다."""
  return {"tasks": [], "filter": {"assignee": assignee, "status": status}}


def update_task_status(task_id: str, status: str) -> dict:
  """업무 상태를 변경한다."""
  return {"task_id": task_id, "status": status}
