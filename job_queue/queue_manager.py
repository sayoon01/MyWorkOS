"""Redis 기반 작업 큐 + 분산락."""

from __future__ import annotations

import json
import os
import uuid
from typing import Any

import redis.asyncio as redis


class QueueManager:
  def __init__(self, redis_url: str | None = None) -> None:
    self._redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379/0")
    self._client: redis.Redis | None = None

  async def connect(self) -> None:
    self._client = redis.from_url(self._redis_url, decode_responses=True)

  async def disconnect(self) -> None:
    if self._client:
      await self._client.aclose()

  @property
  def client(self) -> redis.Redis:
    if self._client is None:
      raise RuntimeError("QueueManager not connected. Call connect() first.")
    return self._client

  async def enqueue(self, queue: str, payload: dict[str, Any]) -> str:
    job_id = str(uuid.uuid4())
    await self.client.hset(f"job:{job_id}", mapping={"status": "pending", "payload": json.dumps(payload)})
    await self.client.lpush(queue, job_id)
    return job_id

  async def acquire_lock(self, key: str, ttl: int = 30) -> bool:
    return bool(await self.client.set(f"lock:{key}", "1", nx=True, ex=ttl))

  async def release_lock(self, key: str) -> None:
    await self.client.delete(f"lock:{key}")
