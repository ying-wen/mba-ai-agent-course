# L9-10 讲义：多智能体系统设计

> **课程**: MBA大模型智能体课程  
> **课时**: 第9-10讲（90分钟）  
> **适用**: 讲师备课 / 学生预习与复习  
> **对应Slides**: `slides-marp/day2-lesson9-10-multi-agent.md`

---

## 本讲核心问题

1. **什么时候需要多Agent？** 单Agent的瓶颈在哪里？
2. **有哪些协作模式？** Pipeline/Supervisor/Debate/Swarm怎么选？
3. **Agent之间如何通信？** 消息传递还是共享状态？
4. **如何选择框架？** AutoGen/CrewAI/LangGraph各有什么特点？

---

## Part 1：为什么需要多Agent？

### 单Agent的瓶颈

当任务变得复杂，单个Agent会遇到三个根本性问题：

**1. 上下文瓶颈**

```
单Agent处理复杂任务:

用户: "帮我做一个完整的市场调研报告"

单Agent尝试:
├── 搜索市场数据 ✓
├── 分析竞争格局 ✓
├── 预测市场趋势 △ (开始疲劳)
├── 撰写执行摘要 △ (质量下降)
├── 设计数据图表 ✗ (上下文溢出)
└── 最终审核校对 ✗ (已经混乱)
```

随着任务推进，上下文不断膨胀，模型的注意力被稀释，输出质量下降。

**2. 角色冲突**

让同一个Agent既"创作"又"审核"，就像让同一个人既写代码又做Code Review——很难保持客观性。

**3. 长链推理脆弱**

多步骤任务中，每一步都有出错概率。如果10步任务每步95%准确率，最终准确率只有60%。

### 多Agent的优势

```
多Agent协作:

用户: "帮我做一个完整的市场调研报告"

Coordinator (协调者)
    │
    ├── Researcher (研究员)
    │   └── 负责数据收集和分析
    │
    ├── Analyst (分析师)
    │   └── 负责竞争格局和趋势
    │
    ├── Writer (撰稿人)
    │   └── 负责报告撰写
    │
    └── Reviewer (审核员)
        └── 负责质量把控
```

**优势**：
- 专业分工，各司其职
- 独立上下文，不会溢出
- 可并行执行，效率更高
- 交叉验证，质量更好

### 何时使用多Agent？

| 场景 | 单Agent | 多Agent |
|------|---------|---------|
| 简单问答 | ✅ | 过度设计 |
| 单一技能任务 | ✅ | 不必要 |
| 需要多视角验证 | ❌ | ✅ |
| 复杂多步骤工作流 | 勉强 | ✅ |
| 长时间运行任务 | 不稳定 | ✅ |

> **MBA视角**：多Agent系统就是"虚拟团队管理"。设计多Agent架构，本质上是在设计组织结构。

---

## Part 2：四种协作模式

### 模式总览

| 模式 | 结构 | 适用场景 | 典型应用 |
|------|------|----------|----------|
| **Pipeline** | 串行流水线 | 步骤明确、依赖清晰 | 内容生产流程 |
| **Supervisor** | 主管调度 | 需要动态决策 | 复杂研究任务 |
| **Debate** | 辩论对抗 | 需要多视角验证 | 风险评估、决策支持 |
| **Swarm/Blackboard** | 群体协作 | 高度并行、涌现式 | 创意生成、探索性任务 |

### 模式1：Pipeline（流水线）

```
Agent A ──► Agent B ──► Agent C ──► 输出

示例: 研究 → 分析 → 撰写 → 审核
```

**特点**：
- 结构清晰，易于理解和调试
- 每个Agent专注单一任务
- 前一步的输出是后一步的输入

**适用场景**：
- 内容生产（采编审发）
- 数据处理（采集清洗分析）
- 审批流程（起草审核发布）

**KPI设计**：
- 每个节点的处理时间
- 每个节点的质量得分
- 整体端到端耗时

### 模式2：Supervisor（主管调度）

```
         Supervisor
              │
    ┌─────────┼─────────┐
    ↓         ↓         ↓
 Worker A  Worker B  Worker C
```

**特点**：
- Supervisor决定任务分配
- 可以动态调度（根据结果决定下一步）
- 支持重试和错误恢复

**Anthropic的实践**：

在[How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)中，Anthropic分享了他们的多Agent研究系统：

- **Lead Agent**：负责规划和协调
- **Subagents**：执行具体的搜索和分析任务
- 每个Subagent可能消耗数万tokens，但只返回精炼的摘要（1000-2000 tokens）

这种架构实现了"关注点分离"——详细的搜索上下文被隔离在子Agent中，主Agent只需要处理精炼后的结果。

### 模式3：Debate（辩论）

```
Agent A ◄───辩论───► Agent B
    │                   │
    └───────┬───────────┘
            ▼
         裁判Agent
            │
            ▼
          结论
```

**特点**：
- 正反方Agent各持立场
- 通过辩论暴露问题和盲点
- 裁判Agent综合判断

**典型应用**：
- 投资决策（多空分析）
- 风险评估（乐观vs悲观）
- 方案比选（A方案vs B方案）

**防跑偏机制**：
- 设置最大辩论轮数
- 要求引用具体证据
- 裁判需要给出判断理由

### 模式4：Swarm/Blackboard（群体协作）

```
         ┌──────────────┐
         │  Blackboard  │
         │  (共享状态)   │
         └──────┬───────┘
                │
    ┌───────────┼───────────┐
    │           │           │
 Agent A    Agent B    Agent C
    │           │           │
    └───────────┴───────────┘
         (并发读写)
```

**特点**：
- 所有Agent共享一个状态空间
- 每个Agent独立判断何时行动
- 结果涌现自群体协作

**适用场景**：
- 创意生成（多角度brainstorm）
- 探索性研究（不确定路径）
- 复杂系统模拟

**挑战**：
- 状态一致性管理
- 死锁和活锁风险
- 结果不确定性

### 模式选择决策树

```
任务结构是否清晰？
    │
    ├── 是 → 步骤是否有严格依赖？
    │         │
    │         ├── 是 → Pipeline
    │         └── 否 → 需要动态调度？
    │                   │
    │                   ├── 是 → Supervisor
    │                   └── 否 → Pipeline并行化
    │
    └── 否 → 需要多视角验证？
              │
              ├── 是 → Debate
              └── 否 → Swarm/Blackboard
```

---

## Part 3：Agent间通信

### 两种通信范式

| 方式 | 做法 | 优点 | 缺点 |
|------|------|------|------|
| **消息传递** | Agent之间发送消息 | 解耦、易追踪 | 需要协议设计 |
| **共享状态** | 读写共享数据结构 | 灵活、信息丰富 | 一致性管理复杂 |

### 消息格式设计

好的消息格式应该包含：

```json
{
  "from": "researcher",
  "to": "analyst",
  "type": "research_result",
  "content": {
    "topic": "中国咖啡市场",
    "findings": [...],
    "confidence": 0.85,
    "sources": [...]
  },
  "metadata": {
    "timestamp": "2026-03-01T00:10:00Z",
    "token_cost": 3500
  }
}
```

### 状态管理

对于复杂任务，需要跟踪：

```python
class TaskState:
    goal: str           # 最终目标
    plan: List[Step]    # 执行计划
    progress: dict      # 当前进度
    artifacts: dict     # 产出物
    errors: List[Error] # 错误记录
```

---

## Part 4：框架选型

### 主流框架对比

| 框架 | 开发者 | 特点 | 适用场景 |
|------|--------|------|----------|
| **AutoGen** | Microsoft | 对话驱动、人机协作强 | 研究、原型 |
| **CrewAI** | 开源社区 | 角色定义清晰、易上手 | 团队协作模拟 |
| **LangGraph** | LangChain | 状态机、可视化、生产级 | 复杂工作流 |

### AutoGen

```python
# 概念示例
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent("assistant", llm_config=config)
user_proxy = UserProxyAgent("user", human_input_mode="NEVER")

# Agent之间通过对话协作
user_proxy.initiate_chat(assistant, message="分析苹果财报")
```

**特点**：
- Agent之间通过消息对话
- 支持人在回路（Human-in-the-loop）
- 代码执行能力强

**局限**：
- 复杂流程控制较难
- 状态管理不够直观

### CrewAI

```python
# 概念示例
from crewai import Agent, Task, Crew

researcher = Agent(
    role="市场研究员",
    goal="收集市场数据",
    backstory="10年市场研究经验..."
)

analyst = Agent(
    role="数据分析师",
    goal="分析市场趋势",
    backstory="专注于消费行业..."
)

task1 = Task(description="调研咖啡市场", agent=researcher)
task2 = Task(description="分析竞争格局", agent=analyst)

crew = Crew(agents=[researcher, analyst], tasks=[task1, task2])
result = crew.kickoff()
```

**特点**：
- 角色定义清晰（Role/Goal/Backstory）
- 任务依赖管理
- 类人团队协作

### LangGraph

```python
# 概念示例
from langgraph.graph import StateGraph

# 定义状态
class ResearchState(TypedDict):
    topic: str
    research: str
    analysis: str
    report: str

# 构建图
workflow = StateGraph(ResearchState)
workflow.add_node("research", research_agent)
workflow.add_node("analyze", analyze_agent)
workflow.add_node("write", write_agent)

workflow.add_edge("research", "analyze")
workflow.add_conditional_edges("analyze", should_continue)
workflow.add_edge("write", END)
```

**特点**：
- 显式状态管理
- 条件分支和循环
- 支持持久化和恢复
- 可视化调试

### 选型建议

| 需求 | 推荐框架 |
|------|----------|
| 快速原型 | CrewAI（最简单） |
| 研究探索 | AutoGen（灵活） |
| 生产部署 | LangGraph（可靠） |
| 自定义需求 | 自研（完全控制） |

---

## Part 5：企业案例

### 案例：多Agent投研系统

**业务场景**：券商需要自动化生成行业研报

**架构设计**：

```
┌─────────────────────────────────────────────────────┐
│                    PM Agent                          │
│                  (项目经理)                          │
└──────────────────────┬──────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         ↓             ↓             ↓
    ┌─────────┐   ┌─────────┐   ┌─────────┐
    │  Data   │   │ Analyst │   │ Writer  │
    │  Agent  │   │  Agent  │   │  Agent  │
    └────┬────┘   └────┬────┘   └────┬────┘
         │             │             │
         └─────────────┴─────────────┘
                       │
              ┌────────┴────────┐
              │  Review Agent   │
              │   (合规审核)     │
              └─────────────────┘
```

**分工**：
- **PM Agent**：接收任务、制定计划、协调进度
- **Data Agent**：搜索新闻、爬取数据、查询数据库
- **Analyst Agent**：财务分析、竞争分析、趋势预测
- **Writer Agent**：结构化撰写、格式化输出
- **Review Agent**：合规检查、事实核验、质量评分

**效果**：
- 研报初稿时间：4小时 → 30分钟
- 数据覆盖：+300%
- 合规问题：-80%

---

## Part 6：落地挑战与最佳实践

### 常见挑战

| 挑战 | 表现 | 解决方案 |
|------|------|----------|
| **协调开销** | Agent之间沟通成本高 | 减少不必要的交互 |
| **错误传播** | 一个Agent出错影响全链 | 错误隔离、重试机制 |
| **调试困难** | 不知道问题出在哪 | 完善日志、可视化追踪 |
| **成本失控** | Token消耗过高 | 预算控制、摘要压缩 |

### 最佳实践

**1. 从简单开始**

```
不要一开始就设计5个Agent
先用2个Agent验证核心流程
逐步添加复杂度
```

**2. 明确职责边界**

```
每个Agent应该：
✅ 有明确的输入和输出
✅ 有清晰的成功标准
✅ 能独立测试
```

**3. 设计观测指标**

```
每个Agent跟踪：
- 调用次数
- 平均耗时
- Token消耗
- 成功率
- 输出质量分
```

**4. 人在回路**

```
关键决策点保留人工确认
- 高风险操作
- 低置信度输出
- 异常情况
```

---

## 课堂实操

### 设计一个多Agent系统（15分钟）

选择以下场景之一，设计多Agent架构：

1. **招聘系统**：简历筛选 → 初面评估 → 报告生成
2. **内容审核**：合规检查 → 质量评分 → 分类标注
3. **客户服务**：意图识别 → 问题解决 → 满意度跟进

需要回答：
- 需要几个Agent？各自职责是什么？
- 采用什么协作模式？
- 如何处理Agent之间的通信？
- 如何处理错误和异常？

---

## 本讲总结

### 核心概念

- **多Agent系统 = 虚拟团队**：设计Agent架构就是设计组织结构
- **四种协作模式**：Pipeline/Supervisor/Debate/Swarm
- **通信方式**：消息传递 vs 共享状态
- **框架选型**：AutoGen(灵活)/CrewAI(简单)/LangGraph(生产)

### 关键决策点

| 问题 | 选择依据 |
|------|----------|
| 单Agent还是多Agent？ | 任务复杂度、是否需要多视角 |
| 哪种协作模式？ | 任务结构、依赖关系 |
| 哪个框架？ | 团队能力、生产要求 |

### MBA关键洞察

1. **多Agent是组织问题，不只是技术问题**
2. **协调成本是真实成本**，不要过度设计
3. **从简单开始**，逐步增加复杂度
4. **可观测性决定可维护性**

---

## 延伸阅读

### 必读
- [Anthropic: How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Lilian Weng: LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)

### 框架文档
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

---

*本讲义最后更新：2026-03-01*
