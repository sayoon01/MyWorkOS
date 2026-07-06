def load_csv(file_path: str) -> dict:
  """CSV/엑셀 파일을 로드해 개요를 반환한다."""
  return {"file_path": file_path, "columns": [], "rows": 0, "missing": {}}


def summarize_stats(file_path: str, columns: list[str] | None = None) -> dict:
  """기초 통계를 계산한다."""
  return {"file_path": file_path, "columns": columns, "stats": {}}


def export_chart(file_path: str, chart_type: str, x: str, y: str) -> dict:
  """차트를 생성한다."""
  return {"chart_type": chart_type, "output_path": f"/data/outputs/{chart_type}.png"}
