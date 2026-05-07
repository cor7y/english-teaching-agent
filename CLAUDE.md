# ETA (English Teaching Agent)

高中英语教学Agent MVP，核心是以学情备忘录为中心的数据闭环。
合作者：Hao（产品/设计）、费杰

## 项目结构

```
eta/
├── CLAUDE.md              # 本文件，项目约定
├── PRD.md                 # 产品需求文档
├── PROGRESS.md            # 工作进度
├── research/              # 调研文档（只读，不修改）
│   ├── 00-taxonomy-and-mvp.md
│   ├── cross-validation-report.md
│   └── 高考英语意图识别知识库框架_claude-sonnet.md
├── knowledge-base/        # 知识库文档（只读，不修改）
│   ├── 01-课标与教学框架.md
│   ├── 02-高考题型与考点分布.md
│   ├── 03-学生常见问题与错误模式.md
│   ├── 04-语法填空专项知识库.md
│   └── 05-意图识别与学情备忘录设计.md
├── src/
│   └── intent/            # 意图识别模块
│       ├── schema.py      # 数据类型定义（IntentType/KnowledgeDomain/ProficiencyLevel）
│       └── classifier.py  # Claude API 调用，核心分类逻辑
├── tests/
│   ├── test_schema.py     # schema 单元测试
│   └── test_classifier.py # 意图识别集成测试（需API key）
└── main.py                # 交互式demo
```

## 技术约定

- 语言：Python 3.11+
- LLM：Claude API（Anthropic SDK）
- 测试：pytest，每个模块写测试
- 代码风格：ruff lint + format

## 分类体系约定

意图识别使用三层分类：Intent Type (K/D/S/M/P/E) × Knowledge Domain (1.x-6.x) × Proficiency Level (L1-L4)。
具体定义见 `knowledge-base/05-意图识别与学情备忘录设计.md`，代码中的分类编号必须与该文档一致。

## 工作流程

- research/ 和 knowledge-base/ 是已完成的调研，只读不改
- 验证命令：`uv run pytest -v`
- 运行demo：`ANTHROPIC_API_KEY=xxx uv run python main.py`
- 改代码前先跑 pytest，改完再跑一遍
- 进度更新写 PROGRESS.md
