from src.intent.schema import IntentType, KnowledgeDomain, ProficiencyLevel, IntentResult


def test_intent_type_values():
    assert IntentType.K.value == "K"
    assert IntentType.D.value == "D"
    assert IntentType.S.value == "S"
    assert IntentType.M.value == "M"
    assert IntentType.P.value == "P"
    assert IntentType.E.value == "E"


def test_intent_type_from_string():
    assert IntentType("K") == IntentType.K
    assert IntentType("E") == IntentType.E


def test_knowledge_domain_covers_mvp_range():
    mvp_domains = [
        "1.3",
        "2.1", "2.2", "2.3", "2.4", "2.5",
        "2.6", "2.7", "2.8", "2.9", "2.10",
    ]
    domain_values = [d.value for d in KnowledgeDomain]
    for code in mvp_domains:
        assert code in domain_values, f"MVP domain {code} missing from KnowledgeDomain"


def test_proficiency_level_order():
    levels = [ProficiencyLevel.L1, ProficiencyLevel.L2, ProficiencyLevel.L3, ProficiencyLevel.L4]
    assert len(levels) == 4


def test_intent_result_construction():
    result = IntentResult(
        intent=IntentType.K,
        domain=KnowledgeDomain.G_2_1,
        level=ProficiencyLevel.L1,
        confidence=0.95,
        reasoning="学生询问时态规则",
    )
    assert result.intent == IntentType.K
    assert result.domain.value == "2.1"
    assert result.confidence == 0.95
