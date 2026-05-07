# ETA — English Teaching Agent

**交互原型：[https://english-teaching-agent.onrender.com](https://english-teaching-agent.onrender.com)**

> 本地运行见下方"运行"章节

---

高中英语教学 Agent MVP。以**学情备忘录**为核心，将学生的自由提问结构化为三层标签——意图类型 × 知识维度 × 能力层级——持续积累学情数据，形成可量化的学习闭环。

合作者：Hao（产品/设计）、费杰

---

## 当前阶段：Phase 1 — 意图识别 PoC

输入一段学生文本 → 输出结构化分类标签 + 置信度 + 推理说明。

**三层分类体系：**

| 层 | 维度 | 范围 |
|----|------|------|
| 意图类型 | K / D / S / M / P / E | 知识查询 / 错误诊断 / 解题求助 / 方法策略 / 练习请求 / 情感表达 |
| 知识维度 | 1.x – 6.x | 词汇 / 语法 / 篇章 / 语用 / 解题策略 / 学习管理 |
| 能力层级 | L1 – L4 | 识记 / 理解 / 应用 / 分析 |

MVP 聚焦题型：**语法填空**（覆盖2.1–2.10语法子类 + 1.3词性构词法）

---

## 运行

需要 Python 3.11+ 和 [uv](https://github.com/astral-sh/uv)。

```bash
# 安装依赖
uv sync

# 启动 Web 原型（浏览器交互界面）
ANTHROPIC_API_KEY=sk-... uv run python server.py

# 命令行 demo（可选）
ANTHROPIC_API_KEY=sk-... uv run python main.py

# 跑测试
uv run pytest -v
```

默认端口 8080，可通过环境变量覆盖：

```bash
PORT=9000 HOST=0.0.0.0 ACCESS_TOKEN=yourtoken uv run python server.py
```

---

## 项目结构

```
eta/
├── server.py              # Web 原型服务（API + 静态文件）
├── main.py                # 命令行交互 demo
├── static/index.html      # 前端页面
├── src/intent/
│   ├── schema.py          # 数据类型定义（IntentType / KnowledgeDomain / ProficiencyLevel）
│   └── classifier.py      # Claude API 调用，核心分类逻辑
├── tests/
│   ├── test_schema.py
│   └── test_classifier.py
├── knowledge-base/        # 分类体系文档（只读）
├── research/              # 调研文档（只读）
├── PRD.md                 # 产品需求
└── PROGRESS.md            # 工作进度
```

---

## 技术栈

- Python 3.11+，标准库 HTTP server（零框架依赖）
- Anthropic SDK（Claude API）
- uv 包管理，ruff lint/format，pytest

---

## 验证目标

| 指标 | 目标 |
|------|------|
| 意图识别准确率（6类） | > 85% |
| 知识维度定位准确率 | > 80% |
| 学情备忘录更新一致性 | 每次交互后状态正确更新 |
