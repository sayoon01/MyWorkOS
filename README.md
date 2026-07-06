# keti-workOS

Google ADK 기반 멀티채널 에이전트 오케스트레이션.
https://sayoon01.github.io/MyWorkOS/


## 전체 아키텍처
<img width="1536" height="1024" alt="ChatGPT Image 2026년 7월 6일 오후 04_40_08" src="https://github.com/user-attachments/assets/164fc980-31a1-4932-9b83-082b657cfd5f" />

```

### 요청 처리 흐름 (Telegram)

```
사용자 메시지
  → telegram_adapter (long polling)
  → Runner.run_async(root_agent)
  → root_agent가 의도 분석 후 transfer_to_agent
  → sub_agent 도구 호출
  → sanitize_user_response (내부 추론 누출 필터)
  → Telegram 회신
```

### 능동 트리거 흐름 (Heartbeat, 준비 중)

```
HeartbeatScheduler (cron)
  → DiffEngine.detect_changes()   # 외부 스냅샷 비교
  → 변경 있으면 Runner.run_async(root_agent, ...)   # TODO
```


### 에이전트 라우팅

| 사용자 요청 유형 | sub_agent |
|------------------|-----------|
| 업무 등록/조회 | `task_agent` |
| 일정/회의/리마인드 | `schedule_agent` |
| 회의록·단건 보고서 | `document_agent` |
| 엑셀/CSV 분석 | `data_agent` |
| 목차·장문 문서·기술문서 | `book_agent` |

> `목차` 키워드가 있으면 `document_agent`가 아닌 **`book_agent`** 로 위임.

### 구성 요소 역할

| 레이어 | 역할 | 상태 |
|--------|------|------|
| `gateway/` | 외부 채널 ↔ ADK Runner 브릿지 | Telegram ✅ |
| `agents/` | LLM 에이전트·도구·위임 | ✅ |
| `job_queue/` | Redis 비동기 작업·락 | 스캐폴드 |
| `heartbeat/` | 주기적 변경 감지 → 에이전트 트리거 | 스캐폴드 |
| `web/` | 운영 대시보드 UI | mock UI |
| `config/` | 채널·환경 설정 | ✅ |

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
