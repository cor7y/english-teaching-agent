"""意图识别集成测试 — 需要 ANTHROPIC_API_KEY 环境变量。
跳过条件：未设置API key时自动skip。
"""

import os
import pytest
from src.intent import classify_intent, IntentType

requires_api = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)

TEST_CASES = [
    # (输入, 期望intent)
    ("定语从句怎么用", IntentType.K),
    ("什么时候用现在完成时", IntentType.K),
    ("have been和had been有什么区别", IntentType.K),
    ("这个句子哪里错了：He have been to Beijing last year.", IntentType.D),
    ("为什么这里不能用that", IntentType.D),
    ("这道语法填空怎么做", IntentType.S),
    ("帮我分析一下这道完形填空", IntentType.S),
    ("语法填空有什么技巧", IntentType.M),
    ("怎么背单词更有效", IntentType.M),
    ("给我出5道非谓语动词的题", IntentType.P),
    ("我想练习定语从句", IntentType.P),
    ("英语太难了学不会", IntentType.E),
    ("我怎么总是做错", IntentType.E),
]


@requires_api
@pytest.mark.parametrize("user_input,expected_intent", TEST_CASES)
def test_intent_classification(user_input: str, expected_intent: IntentType):
    result = classify_intent(user_input)
    assert result.intent == expected_intent, (
        f"输入: {user_input}\n"
        f"期望: {expected_intent.value}, 实际: {result.intent.value}\n"
        f"reasoning: {result.reasoning}"
    )
    assert 0.0 <= result.confidence <= 1.0
