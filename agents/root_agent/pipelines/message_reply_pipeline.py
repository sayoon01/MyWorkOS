from google.adk.agents import LlmAgent, SequentialAgent

from ..common import MODEL, strip_leaked_reasoning

intent_analyzer = LlmAgent(
    model=MODEL,
    name="message_intent_analyzer",
    description="받은 메시지를 분석해 상대방의 의도와 내가 해야 할 일을 정리한다.",
    instruction=(
        "사용자가 전달한 메시지를 보고 다음을 정리하라:\n"
        "1) 상대방이 원하는 것 2) 내가 취해야 할 액션(있다면) 3) 톤(급함/일반/격식)\n"
        "요약만 출력하고 답장은 아직 쓰지 않는다."
    ),
    output_key="message_intent",
    after_model_callback=strip_leaked_reasoning,
)

reply_drafter = LlmAgent(
    model=MODEL,
    name="reply_drafter",
    description="분석된 의도를 바탕으로 답장 초안을 작성한다.",
    instruction=(
        "다음 분석을 바탕으로 답장 초안을 작성하라:\n{message_intent}\n\n"
        "분석된 톤에 맞춰 작성하고, 초안이라는 점을 명시한 뒤 본문만 보여준다."
    ),
    output_key="reply_draft",
    after_model_callback=strip_leaked_reasoning,
)

message_reply_pipeline = SequentialAgent(
    name="message_reply_pipeline",
    description=(
        "받은 메시지/메일을 분석해 답장 초안까지 작성하는 파이프라인. "
        "'이 메시지에 뭐라고 답장할지 초안 써줘' 같은 요청에 사용."
    ),
    sub_agents=[intent_analyzer, reply_drafter],
)
