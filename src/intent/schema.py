from enum import Enum
from dataclasses import dataclass


class IntentType(str, Enum):
    K = "K"  # 知识查询
    D = "D"  # 错误诊断
    S = "S"  # 解题求助
    M = "M"  # 方法策略
    P = "P"  # 练习请求
    E = "E"  # 情感表达


class KnowledgeDomain(str, Enum):
    # 词汇
    V_1_1 = "1.1"  # 词义理解
    V_1_2 = "1.2"  # 词汇辨析
    V_1_3 = "1.3"  # 词性与构词法
    V_1_4 = "1.4"  # 固定搭配与短语
    V_1_5 = "1.5"  # 拼写

    # 语法
    G_2_1 = "2.1"   # 时态与语态
    G_2_2 = "2.2"   # 非谓语动词
    G_2_3 = "2.3"   # 从句
    G_2_4 = "2.4"   # 特殊句式
    G_2_5 = "2.5"   # 主谓一致
    G_2_6 = "2.6"   # 冠词与介词
    G_2_7 = "2.7"   # 代词
    G_2_8 = "2.8"   # 情态动词
    G_2_9 = "2.9"   # 比较级与最高级
    G_2_10 = "2.10"  # 名词形态

    # 语篇
    D_3_1 = "3.1"  # 篇章结构
    D_3_2 = "3.2"  # 衔接手段
    D_3_3 = "3.3"  # 文体特征
    D_3_4 = "3.4"  # 主旨与段意概括

    # 语用
    P_4_1 = "4.1"  # 语境理解
    P_4_2 = "4.2"  # 语言得体性
    P_4_3 = "4.3"  # 中式英语/母语负迁移

    # 题型技能
    T_5_1 = "5.1"  # 阅读理解策略
    T_5_2 = "5.2"  # 七选五策略
    T_5_3 = "5.3"  # 完形填空策略
    T_5_4 = "5.4"  # 语法填空策略
    T_5_5 = "5.5"  # 读后续写策略
    T_5_6 = "5.6"  # 应用文写作策略
    T_5_7 = "5.7"  # 听力策略

    # 学习策略
    L_6_1 = "6.1"  # 记忆方法
    L_6_2 = "6.2"  # 复习规划
    L_6_3 = "6.3"  # 时间管理
    L_6_4 = "6.4"  # 自我监控

    UNKNOWN = "unknown"


class ProficiencyLevel(str, Enum):
    L1 = "L1"  # 识记
    L2 = "L2"  # 理解
    L3 = "L3"  # 应用
    L4 = "L4"  # 分析
    UNKNOWN = "unknown"


@dataclass
class IntentResult:
    intent: IntentType
    domain: KnowledgeDomain
    level: ProficiencyLevel
    confidence: float
    reasoning: str
    thinking: str | None = None
