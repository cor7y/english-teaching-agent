"""ETA 意图识别 demo — 交互式测试"""

from src.intent import classify_intent


EXAMPLES = [
    "定语从句怎么用",
    "这个句子哪里错了：He have been to Beijing last year.",
    "这道语法填空怎么做",
    "怎么背单词更有效",
    "给我出5道非谓语动词的题",
    "英语太难了学不会",
]


def main():
    print("=== ETA 意图识别 PoC ===\n")
    print("示例输入：")
    for i, ex in enumerate(EXAMPLES, 1):
        print(f"  {i}. {ex}")
    print()

    while True:
        user_input = input("请输入（输入q退出）: ").strip()
        if not user_input or user_input.lower() == "q":
            break

        if user_input.isdigit() and 1 <= int(user_input) <= len(EXAMPLES):
            user_input = EXAMPLES[int(user_input) - 1]
            print(f"  → {user_input}")

        try:
            result = classify_intent(user_input)
            print(f"  intent:     {result.intent.value} ({result.intent.name})")
            print(f"  domain:     {result.domain.value}")
            print(f"  level:      {result.level.value}")
            print(f"  confidence: {result.confidence}")
            print(f"  reasoning:  {result.reasoning}")
        except Exception as e:
            print(f"  错误: {e}")
        print()


if __name__ == "__main__":
    main()
