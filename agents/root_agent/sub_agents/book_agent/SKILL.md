# 절차: 책/기술문서 생성 요청 처리
1. doc_type(textbook/guidebook/report/story/general) 불명확하면 먼저 확인
2. topic+doc_type 확보되면 outline_tool로 목차부터 생성
3. 목차 승인 전에는 본문 작성하지 않는다
4. 본문 작성 후 consistency_checker_tool로 검증
5. "보내기/파일로 줘"를 명시했을 때만 export_tool 호출
