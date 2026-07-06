"""ADK MemoryService 연동."""

from __future__ import annotations

from google.adk.memory import InMemoryMemoryService

# 프로덕션에서는 VertexAiMemoryService 등으로 교체
memory_service = InMemoryMemoryService()
