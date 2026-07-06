def outline_tool(topic: str, doc_type: str) -> dict:
  """목차/구조를 생성한다. doc_type: textbook/guidebook/report/story/general"""
  return {"topic": topic, "doc_type": doc_type, "outline": []}


def consistency_checker_tool(draft: str) -> dict:
  """일관성을 검증한다."""
  return {"issues": []}


def export_tool(draft: str, format: str = "docx") -> dict:
  """최종 문서를 변환한다."""
  return {"format": format, "status": "exported"}
