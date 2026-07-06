# keti-workOS

Google ADK 기반 멀티채널 에이전트 오케스트레이션.

## 구조

```
gateway/     # ADK 밖 — Telegram long polling (Phase 1), Slack/Teams 보류
job_queue/   # ADK 밖 — Redis 큐 + 분산락
heartbeat/   # ADK 밖 — cron 기반 능동 트리거
agents/      # ADK 에이전트 (`adk create` 규칙)
```

## 설치

```bash
pip install -e ".[dev]"
cp .env.example .env   # API 키 설정
```

## 실행

```bash
# .env에 TELEGRAM_BOT_TOKEN 설정 후
python -m gateway.webhook_server

# ADK 에이전트 단독 테스트 (CLI)
adk run agents/root_agent
```

채널 on/off는 `config/channels.yaml`에서 관리합니다.

## book_agent 글 유형

| sub_agent  | 용도                              |
|------------|-----------------------------------|
| textbook   | 교재형 — 개념 설명 + 예제 + 문제  |
| guidebook  | 가이드형 — 절차, 사용법, 실무 적용 |
| report     | 보고서형 — 분석, 근거, 결론, 제언 |
| story      | 스토리형 — 소설, 웹툰, 대본       |
| general    | 애매한 일반 글                    |
