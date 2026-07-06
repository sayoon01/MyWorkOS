# 절차: 문서 작성 요청 처리
1. 회의록 요청 → 원본 자료(녹취/메모) 보유 여부 확인, 없으면 draft_meeting_minutes 호출하지 않고 원본 요청
2. 보고서 요청 → 주제/핵심 내용 확인, 없으면 draft_report 호출하지 않고 되묻기
3. 내용 확보되면 draft_meeting_minutes 또는 draft_report 호출, 결과는 항상 "(초안)" 표기
4. "파일로 줘/보내줘"라고 명시했을 때만 export_document 호출
5. 기존 문서 수정 요청이면 덮어쓰기 여부를 먼저 확인
