---
marp: true
theme: default
paginate: true
size: 16:9
backgroundColor: "#f5f5f7"
color: "#1f2937"
style: |
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');
  

  section {
    font-family: 'PingFang SC', 'Hiragino Sans GB', 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
    background: #f5f5f7;
    color: #1f2937;
    padding: 46px 62px;
    line-height: 1.45;
  }

  h1, h2, h3 { margin: 0 0 0.45em 0; }
  h1 { color: #0f172a; font-size: 1.7em; }
  h2 { color: #334155; font-size: 1.25em; }
  h3 { color: #475569; font-size: 1.0em; }

  ul, ol { margin-top: 0.3em; }
  li { margin: 0.18em 0; }

  pre {
    background: #1e293b;
    color: #e2e8f0;
    background: #1e293b;
    color: #e2e8f0;
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 0.58em;
    line-height: 1.4;
  }
  pre code {
    background: transparent;
    color: #e2e8f0;
    padding: 0;
  }
  code {
    background: #dbeafe;
    color: #1e3a8a;
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 0.9em;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.72em;
  }

  th {
    background: #cbd5e1;
    color: #0f172a;
    border: 1px solid #94a3b8;
    padding: 6px 8px;
  }

  td {
    background: #ffffff;
    border: none;
    padding: 6px 8px;
  }

  a { color: #2563eb; text-decoration: underline; }

  .muted { color: #64748b; font-size: 0.85em; }
  .small { font-size: 0.82em; }
  .tiny { font-size: 0.70em; }
  .tag {
    display: inline-block;
    background: #dbeafe;
    color: #1e40af;
    border-radius: 999px;
    padding: 2px 10px;
    margin-right: 8px;
    font-size: 0.72em;
  }
  .card {
    background: #ffffff;
    border: none;
    border-radius: 12px;
    padding: 12px 14px;
  }
---

<!-- _paginate: false -->

# 第9-10课时｜多智能体协作与编排框架
## MBA课程：大模型智能体

<span class="tag">90分钟</span><span class="tag">讲授 + 案例 + 讨论</span>

- 从"单兵作战"到"组织化智能"
- 重点：协作模式、共识机制、实战瓶颈
- 核心问题：**什么时候该用多Agent？用了之后怎么让它稳定运行？**

---

# 你将获得什么

1. **判断力**：什么任务该上多Agent，什么不该
2. **设计力**：四种协作模式 + 三种共识机制
3. **工程直觉**：通信、状态管理的trade-off
4. **选型能力**：2026主流框架对比
5. **风险意识**：多Agent系统的真实挑战与量化数据

---

# 课程地图

| Part | 主题 | 时间 |
|------|------|------|
| **1** | 为什么需要多Agent？ | 10分钟 |
| **2** | 四种协作模式 | 15分钟 |
| **3** | 共识机制——多Agent如何收敛？ | 20分钟 |
| **4** | Agent间通信与状态管理 | 10分钟 |
| **5** | 框架选型 | 10分钟 |
| **6** | 多Agent的真实挑战 | 15分钟 |
| **7** | 总结与关键洞察 | 10分钟 |

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 1

## 为什么需要多Agent？

从能力边界到组织能力

---

# 单Agent的三大瓶颈

### 1. 上下文溢出
信息越多注意力越稀释——市场调研做到一半，前面的数据已被"遗忘"

### 2. 角色冲突
让同一个人既写代码又做Code Review，客观性为零

### 3. 长链推理脆弱
10步任务，每步95%准确率 → 最终准确率仅 **60%**

![augmented-llm](images/augmented-llm.png)

---

# 多Agent的核心优势

| 优势 | 类比 |
|------|------|
| **专业分工** | 每人只做擅长的事 |
| **独立上下文** | 每人有自己的笔记本，不互相干扰 |
| **可并行执行** | 多人同时工作，而非排队等待 |
| **交叉验证** | 独立审计 > 自我审查 |

> **MBA视角**：设计多Agent架构 = 设计虚拟组织结构。角色 + 流程 + 规则。

---

# 何时用 / 不用多Agent？

| 场景 | 建议 | 原因 |
|------|------|------|
| 简单问答、单步生成 | ❌ 单Agent | 多Agent纯粹浪费 |
| 单一技能任务（写代码/写文案） | ❌ 单Agent | 协调成本 > 并行收益 |
| 需要多视角验证（投研、风控） | ✅ 多Agent | 视角差异有真实价值 |
| 大规模并行处理（100份简历） | ✅ 多Agent | 真正的并行加速 |
| 长时间运行（>1小时） | ✅ 多Agent | 避免单Agent上下文溢出 |

**原则**：能用单Agent稳定解决，就先别上多Agent。

---

# 案例：Anthropic多Agent研究系统

**架构**：Lead Agent + 并行Subagents（Orchestrator-Worker模式）

```text
用户查询 → Lead Agent (规划+协调)
              ├→ Subagent 1: 搜索方向A
              ├→ Subagent 2: 搜索方向B
              └→ Subagent 3: 搜索方向C
           ← 汇总精炼 → 最终报告
```

**关键数据**：
- 多Agent vs 单Agent：**BrowseComp提升90.2%**
- Token使用解释 **80%** 的性能差异
- Agent用4×token，多Agent用 **15×token**（vs普通对话）

<div class="tiny muted">来源: <a href="https://www.anthropic.com/engineering/multi-agent-research-system">Anthropic: How We Built Our Multi-Agent Research System</a></div>

---

# Anthropic的七条Prompting原则

1. **像Agent一样思考** — 用Console模拟，观察失败模式
2. **教会Orchestrator如何委派** — 详细任务描述，避免重复/遗漏
3. **匹配查询复杂度** — 简单任务1个Agent，复杂任务10+个
4. **工具设计至关重要** — 差的工具描述会误导Agent
5. **让Agent自我改进** — 用Claude优化Prompt和工具描述
6. **先宽后窄** — 从宽泛搜索开始，逐步聚焦
7. **引导思考过程** — Extended Thinking做可控的草稿纸

> **核心洞察**：多Agent本质是"花足够多的token解决问题"——关键是花在对的地方。

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 2

## 四种协作模式

模式决定系统上限

---

# 四种模式总览

| 模式 | 核心结构 | 优点 | 风险 | 一句话 |
|------|----------|------|------|--------|
| **Pipeline** | 顺序交接 | 可控、清晰 | 累积误差 | 流水线 |
| **Supervisor** | 中心调度 | 灵活、可中断 | 调度瓶颈 | 项目经理 |
| **Debate** | 多角色博弈 | 决策质量高 | 成本高 | 辩论赛 |
| **Swarm** | 去中心化 | 可扩展、鲁棒 | 一致性难 | 群体涌现 |

---

# Pipeline｜内容审核流水线

```text
[采集Agent] → facts.json → [编辑Agent] → draft.md
   → [审核Agent] → reviewed.md → [发布Agent] → published
```

**真实案例**：媒体内容生产的"采编审发"

- 每步有明确的输入/输出契约（Schema）
- 失败只回滚局部，不全链路重跑
- **KPI**：每节点处理时间、重试率、人工介入率

**适用**：输出形态稳定、过程可标准化（报告、SOP、周报）

---

# Supervisor｜Anthropic Lead Agent架构

![orchestrator-workers](images/orchestrator-workers.png)

**Anthropic实践要点**：
- 每个Subagent消耗数万tokens，但只返回 **1000-2000 tokens的精炼摘要**
- 实现"关注点分离"——详细搜索上下文被隔离在子Agent中
- Lead Agent只需处理精炼后的结果

**适用**：需求多变、分支路径多、需要动态决策

---

# Debate｜投资多空分析

```text
🐂 Bull Agent          🐻 Bear Agent
"MACD金叉，加仓"     "PE过高，减持"
    │                       │
    └───── 3轮辩论 ────────┘
              │
              ↓
        ⚖️ Judge Agent
              │
              ↓
    "短期持有，设止损线"
```

**典型应用**：投资决策中的多空分析
- 正方提供看多证据，反方找漏洞和反例
- 裁判综合双方论据，输出"结论 + 置信度 + 风险清单"
- 关键：**限制轮数（3轮最优）**，设定停止条件

**适用**：高风险决策、方案比选、战略评估

---

# Swarm｜Stanford赛博小镇

![autonomous-agent](images/autonomous-agent.png)

**实验**：25个AI Agent在虚拟小镇中自主生活

- 每个Agent有独立的记忆、日程、社交关系
- **没有中心调度**——行为从个体规则中涌现
- 结果：自发组织了情人节派对、互相传播八卦、形成小群体

**启示**：
- 去中心化协作可以产生复杂的涌现行为
- 但一致性和可预测性是最大挑战
- **适用**：大规模探索、创意生成、研究性模拟

<div class="tiny muted">来源: Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (Stanford, 2023)</div>

---

# 模式选择决策树

```text
你的任务是什么类型？
│
├── 步骤固定、依赖清晰？ ──→ Pipeline
│
├── 路径多变、需要动态调度？ ──→ Supervisor
│
├── 需要多视角验证？ ──→ Debate
│
└── 大规模探索、无固定路径？ ──→ Swarm

实际上? → 组合拳：
  前段 Supervisor 分解 → 中段 Debate 复核 → 后段 Pipeline 产出
```

> **MBA类比**：没有"最好的组织架构"，只有"最适合业务阶段的架构"。

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 3

## 共识机制——多Agent如何收敛？

当多个Agent给出矛盾结论时，谁说了算？

---

# 问题引入：CEO的烦恼

> 你是投研团队的CEO。三位分析师刚交了报告：

| 分析师 | 结论 | 置信度 |
|--------|------|--------|
| Agent A（基本面） | "特斯拉PE过高，**减持**" | 90% |
| Agent B（技术面） | "MACD金叉，**加仓**" | 55% |
| Agent C（情绪面） | "市场乐观，**短期看涨**" | 55% |

**问题**：研报怎么写？

- 简单投票？→ 2:1 加仓
- 但置信度最高的专家说减持……
- **这不是边缘情况——这是多Agent系统的常态**

---

# 三种决策机制对比

| 机制 | 原理 | 速度 | 深度 | 适用场景 |
|------|------|------|------|----------|
| **投票 Voting** | 多数票胜出 | ⚡最快 | 浅 | 事实性判断 |
| **辩论 Debate** | 多轮辩论+裁判 | 🔄中等 | 深 | 复杂分析 |
| **共识 Consensus** | 讨论直到一致 | 🐢最慢 | 中 | 需要buy-in的决策 |

<div class="tiny muted">参考: <a href="https://arxiv.org/abs/2502.19130">ACL 2025: Voting or Consensus? Decision-Making in Multi-Agent Debate</a></div>

---

# ACL 2025论文核心发现

**论文**：系统评估了7种决策协议在知识和推理任务上的表现

| 发现 | 数据 |
|------|------|
| 投票在推理任务上 | 比其他协议提升 **13.2%** |
| 共识在知识任务上 | 比其他协议提升 **2.8%** |
| 增加Agent数量 | ✅ 提升性能 |
| 增加讨论轮数再投票 | ❌ **反而降低**性能 |

**最关键的发现**：
- 辩论 **2-3轮** 质量最优，超5轮质量反而下降
- Agent在辩论中倾向"**社会性从众**"——放弃正确立场向多数派妥协
- **异构Agent**（不同模型/不同角色）效果**显著优于**同构Agent

---

# 投票：快但危险

```python
# 简单多数投票: buy 赢 (2:1)
votes = {"A": "sell", "B": "buy", "C": "buy"}
# 结果: buy

# 但 Agent A 有 90% 置信度，B和C只有 55%！
# 多数投票忽略了置信度差异 → 潜在错误决策
```

**投票适合**：有唯一正确答案的事实判断
- "这个数据是否正确？"
- "代码是否通过测试？"

**投票不适合**：需要深度分析的开放性问题

---

# 加权投票 > 简单投票

```python
# Confidence-weighted voting
weighted_votes = {
    "A": {"decision": "sell", "confidence": 0.90, "domain_score": 0.85},
    "B": {"decision": "buy",  "confidence": 0.55, "domain_score": 0.70},
    "C": {"decision": "buy",  "confidence": 0.55, "domain_score": 0.60},
}

sell_score = 0.90 * 0.85                        # = 0.765
buy_score  = (0.55 * 0.70 + 0.55 * 0.60) / 2   # = 0.358

# sell_score (0.765) >> buy_score (0.358)
# 结论反转！加权后 sell 胜出
```

**洞察**：不加权的投票在Agent系统中很危险——低置信度的"多数"可以压倒高置信度的少数。

---

# Confabulation Consensus：投票的隐藏陷阱

![evaluator-optimizer](images/evaluator-optimizer.png)

**AgentAuditor论文**（2026）揭示的核心问题：

> 多数投票丢弃了推理过程的**证据结构**，在"confabulation consensus"下特别脆弱——Agent共享相关偏见，收敛到**相同的错误推理路径**。

**解法**：AgentAuditor
- 不投票，而是在**推理树**上做路径搜索
- 在关键分歧节点比较推理分支
- 将"全局裁决"转化为"局部验证"
- 提出ACPO（Anti-Consensus Preference Optimization）：**奖励有证据的少数派，而非流行的错误**

**结果**：比多数投票提升 **5%**，比LLM-as-Judge提升 **3%**

<div class="tiny muted">来源: <a href="https://arxiv.org/abs/2602.09341">AgentAuditor: Auditing Multi-Agent LLM Reasoning Trees (2026)</a></div>

---

# 辩论的四大陷阱

| 陷阱 | 表现 | 解法 |
|------|------|------|
| **社会性从众** | Agent放弃正确观点，向多数妥协 | 设"坚守阈值"，高置信度不让步 |
| **循环论证** | A引用B的结论，B又引用A | 强制所有论据指向外部证据源 |
| **权威偏见** | "专家"标签被过度权重 | 匿名辩论 + 最后揭示身份 |
| **信息级联** | 先发言者影响所有后续Agent | 并行独立分析 → 再交叉辩论 |

> **设计原则**：让Agent独立思考，再交叉验证——**独立性是辩论质量的基石**。

---

# 混合策略：根据任务类型动态选择

```python
def choose_consensus(task_type, time_budget, num_agents):
    if task_type == "factual":
        # 事实判断 → 加权投票（快速准确）
        return weighted_vote(agents, weights="domain_expertise")

    elif task_type == "analytical":
        # 分析推理 → 辩论（2-3轮，异构Agent）
        return debate(agents, max_rounds=3, heterogeneous=True)

    elif task_type == "strategic":
        if time_budget > "2_hours":
            # 有时间 → 共识收敛（需要buy-in）
            return consensus(agents, convergence_threshold=0.8)
        else:
            # 时间紧 → 辩论 + 人工裁决
            return human_review(debate(agents, max_rounds=2))

    else:
        # 紧急情况 → Supervisor直接裁决
        return supervisor_decision(lead_agent)
```

---

# MBA类比：日常运营、战略方向、组织变革

| 场景 | 企业做法 | 多Agent机制 |
|------|----------|------------|
| **日常运营** | 董事会表决 | 投票（加权） |
| **战略方向** | 咨询公司方法论 | 辩论（2-3轮） |
| **组织变革** | 战略规划会 | 共识收敛 |
| **危机处理** | CEO拍板 | Supervisor裁决 |

> 设计多Agent系统的决策机制，**本质上是在设计虚拟组织的治理结构**。

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 4

## Agent间通信与状态管理

多Agent系统的"神经系统"

---

# 三种通信模式

| 模式 | 特点 | 适用 | 企业类比 |
|------|------|------|----------|
| **消息传递** | 点对点/总线，松耦合 | 明确的请求-响应场景 | 发邮件 |
| **共享状态** | 共享记忆空间，读写并发 | 需要全局视图 | 共享文档 |
| **事件驱动** | 订阅-发布，异步响应 | 实时流程/异步任务 | Slack通知 |

---

# 消息格式：最小可行协议

```json
{
  "message_id": "uuid-001",
  "from": "research_agent",
  "to": "analyst_agent",
  "task_id": "task_2026_001",
  "type": "EVIDENCE",
  "payload": {
    "facts": ["Tesla Q4 revenue: $25.7B", "PE ratio: 68.3x"],
    "sources": ["sec.gov/filing/xxx", "yahoo.finance/tsla"]
  },
  "confidence": 0.82,
  "timestamp": "2026-03-13T10:30:00Z"
}
```

**五种消息类型**：`PLAN` → `EVIDENCE` → `CRITIQUE` → `DECISION` → `ALERT`

统一类型 = 可追踪、可审计、可自动化。

---

# 状态管理的Trade-off

| 维度 | 消息传递 | 共享状态 | 事件驱动 |
|------|----------|----------|----------|
| 实现复杂度 | 低 | 中 | 高 |
| 扩展性 | 好 | 需要锁机制 | 好 |
| 一致性 | 最终一致 | 强一致 | 最终一致 |
| 调试难度 | 容易追踪 | 中等 | 难 |
| 典型框架 | AutoGen | LangGraph | OpenClaw |

**实践建议**：
- 短期状态存流程上下文（会话级）
- 长期状态存知识库和策略库（系统级）
- **避免把所有历史对话无差别塞进Prompt**

---

# 上下文压缩：不是所有信息都值得保留

```text
传统: 全量聊天历史 → 压缩 → 关键信息丢失

结构化方式: 聊天历史 → 分类 → 选择性保留

保留优先级:
  1. 用户指令 (user_instruction)     → 永远保留
  2. 关键决策 (assistant_decision)   → 高优先
  3. 错误记录 (error)               → 中优先
  4. 工件引用 (artifact_reference)   → 中优先
  5. 闲聊/思考过程                  → 可压缩/丢弃
```

> 将上下文从"聊天历史"升级为"**可计算的协作状态**"。

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 5

## 框架选型（2026）

先定模式，再选框架

---

# 2026主流框架对比

| 框架 | 核心范式 | 优势 | 适用场景 | 学习曲线 |
|------|----------|------|----------|----------|
| **AutoGen** | 对话协作 | 多角色讨论自然 | 辩论/评审 | 中 |
| **CrewAI** | 角色+任务 | 上手快、业务友好 | 流程化执行 | 低 |
| **LangGraph** | 状态图编排 | 可控、可恢复、可审计 | 企业级流程 | 中高 |
| **AgentScope** | 分布式多Agent | 大规模、可扩展 | 研究/大型系统 | 中高 |

<div class="tiny muted">各框架能力随版本快速变化，以官方最新文档为准。</div>

---

# 治理维度对比

| 维度 | AutoGen | CrewAI | LangGraph | AgentScope |
|------|---------|--------|-----------|------------|
| 流程控制 | 中 | 中 | **高** | 中高 |
| 可观测性 | 中 | 中 | **高** | 中 |
| 企业治理 | 中 | 中高 | **高** | 中 |
| 错误恢复 | 低 | 中 | **高** | 中 |
| 社区生态 | **高** | 高 | 高 | 中 |

---

# 选型决策矩阵

| 你的需求 | 推荐 |
|----------|------|
| 快速验证PoC | CrewAI → 几天内出Demo |
| 企业级流程、强治理 | LangGraph → 状态图可审计 |
| 多角色辩论/讨论 | AutoGen → 对话模式自然 |
| 大规模分布式Agent | AgentScope → 可扩展架构 |
| 工程效率（编码） | Claude Code / Codex CLI → 终端Agent |
| 跨职能协同 | OpenClaw → CEO架构分工 |

> **原则**：框架选型要服务业务目标与治理要求——不是"哪个框架最酷"。

---

# 低代码/No-Code产品层

| 产品 | 定位 | 适合 |
|------|------|------|
| **Dify** | 可视化工作流 | 业务快速落地，非技术团队 |
| **Coze** | Bot平台/工作流 | 运营与增长场景 |
| **Cursor** | AI编程IDE | 人机共编，开发团队 |

**2026选型不再是"单一框架之争"**：
- 产品层决定用户体验上限
- 框架层决定工程质量下限
- 治理层决定能否上生产

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 6

## 多Agent的真实挑战

框架解决了"怎么搭"，但没解决"怎么稳定运行"

---

# OMAO视角：七个结构性缺口

| # | 缺口 | 影响 | 企业类比 |
|---|------|------|----------|
| A | 上下文无结构化状态 | 压缩时关键信息丢失 | **会议纪要没有重点** |
| B | 子Agent孤立执行 | delegation ≠ collaboration | **派了活就不管了** |
| C | 无共享任务状态层 | 不知道谁在干什么 | **团队没有项目管理工具** |
| D | 无异步事件机制 | 只能手动轮询 | **没有消息通知系统** |
| E | 无冲突解决协议 | 矛盾结果无仲裁 | **多份报告不知道怎么合** |
| F | 无系统稳定性保障 | 死循环、级联阻塞 | **没有断路器和熔断** |
| G | 无动态任务分解 | 依赖人工规划 | **没有HR和项目经理** |

<div class="tiny muted">来源: OMAO (OpenClaw Multi-Agent Optimization) 项目</div>

---

# 瓶颈1：派发成本高

```text
理想:  用户请求 → CEO → 子Agent → 结果     Token: 1x

现实:  用户请求 → CEO理解(2K)
       → 分析需要几个Agent(1K)
       → 构造每个Agent上下文(3K × N)
       → 子Agent各自执行(5K × N)
       → CEO汇总(3K)                       Token: 5-10x
```

**Anthropic数据**：每个Subagent消耗**数万tokens**，但只返回1000-2000 tokens摘要

> 简单任务用多Agent反而更贵更慢！

---

# 瓶颈2：上下文传递损失

CEO的完整理解 → 传递给子Agent → 信息保真度约 **60-70%**

| 损失类型 | 例子 |
|----------|------|
| 隐含知识丢失 | CEO知道用户偏好，子Agent不知道 |
| 格式损失 | 结构化信息被扁平化为prompt文本 |
| 优先级丢失 | 什么重要什么不重要，需要重新推断 |
| 约束丢失 | "不要超过3页"这类约束常被遗忘 |

**解法**：结构化输出契约（Schema） + 显式传递约束列表

---

# 瓶颈3：结果汇聚弱

```text
子Agent A: 5000字详细分析
子Agent B: 3张表格 + 2段总结
子Agent C: 10个数据点 + 1段结论

CEO需要汇总成一份报告:
- 格式不统一 → 需要额外处理
- 观点矛盾   → 需要裁决（回到共识问题）
- 粒度不同   → 需要对齐
- 引用来源   → 需要合并去重
```

**实测**：汇总步骤消耗的Token ≈ 所有子Agent执行的总和

---

# 瓶颈4：质量门禁虚化

```text
设计时: "每个Agent输出都经过Reviewer审核"

现实: Reviewer说 "LGTM, 看起来不错" (90%的情况)
```

**为什么？**
1. Reviewer缺乏足够上下文判断对错
2. LLM的"讨好倾向"——倾向肯定而非否定
3. 没有ground truth做对比

**四种强化策略**：

| 策略 | 做法 |
|------|------|
| 对抗性验证 | 专门找茬的"红队"Agent |
| Rubric评分 | 按标准逐项量化打分 |
| 交叉验证 | 让Agent B审Agent A的工作 |
| 人在回路 | 关键节点保留人工审核 |

---

# 与Codex / Claude Code Teams的对比

| 维度 | Claude Code Teams | Codex Multi-Agent | 理想多Agent系统 |
|------|-------------------|-------------------|-----------------|
| 核心目标 | 协作编码/研究 | 并行编码执行 | 长期assistant协作 |
| 时间尺度 | 分钟~小时 | 分钟~小时 | **秒~天** |
| 协作核心 | task list + peer msg | spawn/wait | 结构化状态+事件驱动 |
| 关键挑战 | 并行协调 | 吞吐 | **连续性+稳定性** |

> Codex/Claude Code优先解决"同一任务如何并行做快"；
> 长期助手需要解决"如何在**不失控**的前提下稳定协作"。

---

# 关键判断

## 多Agent不是银弹

**《人月神话》对多Agent同样成立**：增加Agent不一定加速任务。

协调成本是真实成本：
- 每多一个Agent，派发/汇聚各增3-5K tokens
- 信息传递损失30-40%
- 质量门禁容易虚化

### 5人精锐 > 20人松散团队

不要追求Agent数量——追求**每个Agent的产出质量和协作效率**。

![parallelization](images/parallelization.png)

---

<!-- _backgroundColor: #0f172a -->
<!-- _color: #f1f5f9 -->

# Part 7

## 总结与关键洞察

---

# 核心概念回顾

| 概念 | 关键要点 |
|------|----------|
| **何时多Agent** | 任务复杂度高 + 需要多视角 + 可并行 |
| **四种模式** | Pipeline / Supervisor / Debate / Swarm — 模式先于框架 |
| **共识机制** | 投票（快浅）/ 辩论（深贵）/ 共识（全慢）— 动态选择 |
| **通信设计** | 消息格式统一、状态显式化、避免黑箱 |
| **框架选型** | 业务需求 → 治理要求 → 技术选型 |
| **真实挑战** | 派发成本、上下文损失、汇聚弱、门禁虚化 |

---

# MBA关键洞察

### 1. 多Agent = 虚拟组织设计
设计Agent系统的本质就是设计组织结构。CEO/PM/专家/审计，和真实公司一样。

### 2. 共识机制 = 治理结构
投票/辩论/共识不是技术选择——是**治理哲学**的选择。

### 3. 协调税是真实成本
多Agent的隐性成本很容易被低估。先算清ROI，再决定是否上多Agent。

### 4. 多数投票可能是陷阱
当Agent共享偏见时，投票只会放大错误。**证据质量 > 投票人数**。

### 5. 先跑通单Agent，再考虑多Agent
过度设计是最常见的失败模式。

---

# 延伸阅读

### 学术论文
- [Voting or Consensus? Decision-Making in Multi-Agent Debate](https://arxiv.org/abs/2502.19130) — ACL 2025，共识机制系统评估
- [AgentAuditor: Auditing Multi-Agent LLM Reasoning Trees](https://arxiv.org/abs/2602.09341) — Confabulation Consensus问题

### 工程实践
- [Anthropic: How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system) — Lead Agent + Subagents架构
- [LangChain: Choosing the Right Multi-Agent Architecture](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/)
- [OpenAI: A Practical Guide to Building AI Agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)

### 框架文档
- [AutoGen](https://www.microsoft.com/en-us/research/project/autogen/) · [CrewAI](https://www.crewai.com/) · [LangGraph](https://langchain-ai.github.io/langgraph/) · [AgentScope](https://github.com/modelscope/agentscope)

---

# 课后作业

**题目**：设计一个多Agent投研分析系统

要求：
1. 至少4个角色，说明分工和协作模式
2. 设计共识机制——当Agent意见分歧时如何裁决？
3. 给出消息Schema + 一条完整的消息流示例
4. 评估ROI：多Agent vs 单Agent的成本和质量对比
5. 提交：架构图 + 关键Prompt + 决策日志

---

<!-- _paginate: false -->

# 谢谢

## 第9-10课时结束

<span class="muted">下节课：MCP协议与工具生态（从Agent到可调用能力网络）</span>
