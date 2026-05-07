import json
import os
import re
import anthropic
from .schema import IntentResult, IntentType, KnowledgeDomain, ProficiencyLevel

SYSTEM_PROMPT = """\
你是一个高中英语教学意图识别系统。你的任务是分析学生的输入，输出结构化分类标签。

## 第一层：问题性质（intent）
- K: 知识查询 — 学生想了解某个知识点的规则/定义/用法。如"定语从句怎么用""什么时候用现在完成时"
- D: 错误诊断 — 学生提交了句子/答案，想知道哪里错了、为什么错。如"这个句子哪里错了""为什么这里不能用that"
- S: 解题求助 — 学生遇到具体题目，需要解题指导。如"这道语法填空怎么做""帮我分析一下这道完形"
- M: 方法策略 — 学生想了解学习方法、解题技巧、复习规划。如"怎么背单词""语法填空有什么技巧"
- P: 练习请求 — 学生想做练习题或自测。如"给我出几道题""我想练习非谓语动词"
- E: 情感表达 — 学生表达学习中的情绪。如"英语太难了""我怎么总是做错"

## 第二层：知识维度（domain）
1.1 词义理解 | 1.2 词汇辨析 | 1.3 词性与构词法 | 1.4 固定搭配与短语 | 1.5 拼写
2.1 时态与语态 | 2.2 非谓语动词 | 2.3 从句 | 2.4 特殊句式 | 2.5 主谓一致
2.6 冠词与介词 | 2.7 代词 | 2.8 情态动词 | 2.9 比较级与最高级 | 2.10 名词形态
3.1 篇章结构 | 3.2 衔接手段 | 3.3 文体特征 | 3.4 主旨与段意概括
4.1 语境理解 | 4.2 语言得体性 | 4.3 中式英语/母语负迁移
5.1 阅读理解策略 | 5.2 七选五策略 | 5.3 完形填空策略 | 5.4 语法填空策略
5.5 读后续写策略 | 5.6 应用文写作策略 | 5.7 听力策略
6.1 记忆方法 | 6.2 复习规划 | 6.3 时间管理 | 6.4 自我监控
- 如果无法确定具体知识维度，使用 "unknown"

## 第三层：能力层级（level）
- L1 识记: 知道规则/定义
- L2 理解: 能解释和区分
- L3 应用: 能在新语境中使用
- L4 分析: 能识别错误和原因
- 如果不适用（如情感表达、方法策略），使用 "unknown"

## 输出格式
严格输出JSON，不要其他内容：
{"intent": "K", "domain": "2.1", "level": "L2", "confidence": 0.9, "reasoning": "一句话解释"}
"""


def classify_intent(
    user_input: str,
    *,
    client: anthropic.Anthropic | None = None,
    model: str = "claude-sonnet-4-6",
) -> IntentResult:
    if client is None:
        client = anthropic.Anthropic(
            base_url=os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com"),
        )

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_input}],
    )

    thinking_block = next((b for b in response.content if b.type == "thinking"), None)
    thinking_text = thinking_block.thinking if thinking_block else None

    text_block = next((b for b in response.content if b.type == "text"), None)
    if text_block is None:
        raise ValueError(f"No text block in response: {[(b.type, type(b).__name__) for b in response.content]}")
    raw = text_block.text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raw = re.sub(r'(\d)"+(\s*[,}])', r'\1"\2', raw)
        raw = re.sub(r':\s*(\d+\.?\d*)"(\s*[,}])', r': \1\2', raw)
        data = json.loads(raw)

    return IntentResult(
        intent=IntentType(data["intent"]),
        domain=KnowledgeDomain(data["domain"]),
        level=ProficiencyLevel(data["level"]),
        confidence=float(data["confidence"]),
        reasoning=data["reasoning"],
        thinking=thinking_text,
    )
