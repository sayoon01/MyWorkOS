def draft_meeting_minutes(title: str, raw_notes: str) -> dict:
  """회의록 초안을 생성한다."""
  return {"title": title, "draft": f"[{title}] 회의록(초안)\n\n{raw_notes}"}


def draft_report(topic: str, content: str) -> dict:
  """보고서 초안을 생성한다."""
  return {"topic": topic, "draft": f"[{topic}] 보고서(초안)\n\n{content}"}


def export_document(draft: str, format: str = "docx") -> dict:
  """초안을 파일로 변환한다."""
  return {"format": format, "status": "exported"}
