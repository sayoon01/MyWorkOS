"""외부 상태 스냅샷 비교 — 변경 감지."""

from __future__ import annotations

from typing import Any


class DiffEngine:
  def __init__(self) -> None:
    self._last_snapshot: dict[str, Any] = {}

  async def detect_changes(self) -> list[dict[str, Any]]:
    current = await self._fetch_snapshot()
    changes: list[dict[str, Any]] = []
    for key, value in current.items():
      if self._last_snapshot.get(key) != value:
        changes.append({"key": key, "old": self._last_snapshot.get(key), "new": value})
    self._last_snapshot = current
    return changes

  async def _fetch_snapshot(self) -> dict[str, Any]:
    # TODO: 실제 데이터 소스(Notion, DB, 파일 등)에서 스냅샷 수집
    return {}
