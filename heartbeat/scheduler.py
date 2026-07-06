"""cron pulse → Runner 세션 시작."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from heartbeat.diff_engine import DiffEngine

logger = logging.getLogger(__name__)


class HeartbeatScheduler:
  def __init__(self, interval_seconds: int = 300) -> None:
    self._interval = interval_seconds
    self._diff = DiffEngine()
    self._running = False

  async def start(self) -> None:
    self._running = True
    logger.info("Heartbeat scheduler started (interval=%ds)", self._interval)
    while self._running:
      await self._pulse()
      await asyncio.sleep(self._interval)

  async def stop(self) -> None:
    self._running = False

  async def _pulse(self) -> None:
    now = datetime.utcnow().isoformat()
    changes = await self._diff.detect_changes()
    if changes:
      logger.info("[%s] Detected %d changes — triggering agent session", now, len(changes))
      # TODO: Runner.run_async(root_agent, session_id=..., message=...)
