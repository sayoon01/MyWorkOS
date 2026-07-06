# Heartbeat

능동 트리거 시스템. cron pulse가 `diff_engine`으로 외부 상태 변경을 감지하면 ADK Runner 세션을 시작한다.

## 흐름

```
scheduler (cron) → diff_engine.detect_changes() → 변경 있으면 Runner.run_async()
```

## 설정

- `interval_seconds`: pulse 주기 (기본 300초)
- 감시 대상은 `diff_engine._fetch_snapshot()` 에서 정의
