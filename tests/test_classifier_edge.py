"""边界case和模糊输入测试 — 需要 ANTHROPIC_API_KEY。"""

import os
import pytest
from src.intent import classify_intent, IntentType, KnowledgeDomain

requires_api = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)

EDGE_CASES = [
    # 口语化/简短输入
    ("非谓语", IntentType.K),
    ("虚拟语气", IntentType.K),
    # 混合意图 — 以主意图为准
    ("定语从句总是搞不懂，能出几道题让我练练吗", IntentType.P),
    ("这道题我做错了，能讲讲非谓语动词的用法吗", IntentType.K),
    # 包含具体题目内容
    ("The book _____(write) by him is very popular. 这里填什么", IntentType.S),
    # 带上下文的错误诊断
    ("我写了 I am agree with you，老师说不对，为什么", IntentType.D),
    # 纯英文输入
    ("What is the difference between which and that in relative clauses?", IntentType.K),
]


@requires_api
@pytest.mark.parametrize("user_input,expected_intent", EDGE_CASES)
def test_edge_case_intent(user_input: str, expected_intent: IntentType):
    result = classify_intent(user_input)
    assert result.intent == expected_intent, (
        f"输入: {user_input}\n"
        f"期望: {expected_intent.value}, 实际: {result.intent.value}\n"
        f"reasoning: {result.reasoning}"
    )


DOMAIN_CASES = [
    ("现在完成时和过去完成时有什么区别", "2.1"),
    ("什么时候用to do，什么时候用doing", "2.2"),
    ("which和that在定语从句里怎么选", "2.3"),
    ("什么时候要用倒装句", "2.4"),
    ("名词变形容词有什么规律", "1.3"),
]


@requires_api
@pytest.mark.parametrize("user_input,expected_domain", DOMAIN_CASES)
def test_domain_classification(user_input: str, expected_domain: str):
    result = classify_intent(user_input)
    assert result.domain.value == expected_domain, (
        f"输入: {user_input}\n"
        f"期望domain: {expected_domain}, 实际: {result.domain.value}\n"
        f"reasoning: {result.reasoning}"
    )
