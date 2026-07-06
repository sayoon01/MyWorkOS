"""Teams 어댑터 — Phase 2 보류."""

from __future__ import annotations

from typing import Any


class TeamsAdapter:
  """Microsoft Teams Bot Framework 어댑터 (미구현)."""

  async def parse_event(self, payload: dict[str, Any]) -> dict[str, Any]:
    raise NotImplementedError("Teams adapter is not enabled in Phase 1")
