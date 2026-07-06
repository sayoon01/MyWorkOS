# Heartbeat

능동 트리거 시스템. asyncio 폴링으로 외부 상태 변경을 감지하면 ADK Runner 세션을 시작한다.

## 감시 대상

- **파일:** `/data/uploads/*.csv` (신규 파일 감지 → `data_agent` 자동 실행)
- **일정:** 매일 09:00 KST → `task_agent`에게 "오늘 마감 업무" 조회 요청

## 주기

| 트리거 | 주기 |
|--------|------|
| 파일 감지 | 5분 간격 pulse (`HEARTBEAT_CHECK_INTERVAL_SEC`, 기본 300) |
| 아침 브리핑 | 1일 1회 09:00 KST |

## 흐름

```
scheduler (asyncio loop)
  → check_new_files() / daily_briefing()
  → notify_via_bot() → Runner.run_async(root_agent)
  → (TODO) Telegram push
```

## 실행

### 통합 모드 (권장) — Telegram + Heartbeat 한 프로세스

```bash
# .env: HEARTBEAT_TARGET_USER_ID, TELEGRAM_BOT_TOKEN 설정
python -m gateway.webhook_server
```

`push_message`가 같은 프로세스의 봇 인스턴스를 사용해 Telegram으로 push합니다.

### 분리 모드 — heartbeat만 단독 실행

```bash
python -m heartbeat.scheduler
```

`TELEGRAM_BOT_TOKEN`이 있으면 Bot API(httpx)로 직접 `sendMessage`합니다.

## 환경변수

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `HEARTBEAT_TARGET_USER_ID` | (필수) | 알림·에이전트 세션 대상 사용자 ID |
| `HEARTBEAT_UPLOAD_DIR` | `data/uploads` | CSV 감시 디렉터리 (프로젝트 루트 기준 상대경로 가능) |
| `HEARTBEAT_CHECK_INTERVAL_SEC` | `300` | 폴링 주기(초). 로컬 테스트는 `10` 권장 |

## Phase 2 이후

- `diff_engine.py`: Notion/DB 등 스냅샷 비교로 확장
- Telegram `bot.send_message` 연동으로 터미널 출력 대신 push
