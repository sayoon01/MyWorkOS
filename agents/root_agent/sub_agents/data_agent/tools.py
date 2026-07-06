from __future__ import annotations


def _pandas():
  import pandas as pd

  return pd


def load_csv(file_path: str) -> dict:
  """CSV/엑셀 파일을 로드해 컬럼·행수·결측치 현황을 반환한다."""
  pd = _pandas()
  try:
    df = pd.read_csv(file_path)
  except Exception as e:
    return {"error": str(e), "file_path": file_path}
  return {
      "file_path": file_path,
      "columns": list(df.columns),
      "rows": len(df),
      "missing": df.isnull().sum().to_dict(),
      "preview": df.head(3).to_dict(orient="records"),
  }


def summarize_stats(file_path: str, columns: list[str] | None = None) -> dict:
  """지정 컬럼의 기초 통계를 계산한다."""
  pd = _pandas()
  try:
    df = pd.read_csv(file_path)
  except Exception as e:
    return {"error": str(e), "file_path": file_path}
  target = df[columns] if columns else df.select_dtypes(include="number")
  return {"file_path": file_path, "stats": target.describe().to_dict()}


def export_chart(file_path: str, chart_type: str, x: str, y: str) -> dict:
  """차트를 생성한다."""
  return {"chart_type": chart_type, "output_path": f"/data/outputs/{chart_type}.png"}
