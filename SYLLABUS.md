# 📋 课程大纲 | 大模型智能体 (LLM Agents)

**学分**: 2  
**课时**: 16 (2天 × 8课时)  
**授课语言**: 中文 (技术术语英文)

---

## 第一天: 从大模型到单智能体

### 📚 第1-2课时: 大语言模型基础与Prompt工程

**学习目标**:
- 理解Transformer架构和大模型工作原理
- 掌握Prompt工程的核心技巧
- 区分不同模型的能力边界

**内容大纲**:

1. **大模型演进史** (20min)
   - GPT系列: GPT-3 → GPT-4 → GPT-5
   - Claude系列: Claude 2 → Claude 3 → Claude 4.5/4.6
   - 开源生态: LLaMA → Qwen → GLM-5
   - 中国模型: DeepSeek R1/R2, Kimi K2.5

2. **核心概念** (25min)
   - Token、上下文窗口、Temperature
   - 涌现能力 (Emergent Abilities)
   - Scaling Laws与Chinchilla定律
   - Reasoning Models: o1/o3, DeepSeek R1

3. **Prompt工程实战** (40min)
   - Zero-shot、Few-shot、Chain-of-Thought
   - 角色设定与系统提示词
   - 结构化输出 (JSON Mode)
   - 提示词注入攻击与防御

4. **现场演示**: Claude vs GPT-5 能力对比

**实验环节**: Lab 1 - Prompt Engineering Playground

---

### 📚 第3-4课时: 大模型工作流：从链式到图式

**学习目标**:
- 理解LLM应用的演进路径
- 掌握主流工作流框架
- 学会设计复杂的LLM应用

**内容大纲**:

1. **工作流演进** (20min)
   - 单次调用 → 链式调用 → DAG → 循环图
   - 为什么需要工作流？
   - 工作流 vs Agent的边界

2. **LangChain深度解析** (25min)
   - LCEL (LangChain Expression Language)
   - Chain、Memory、Retriever
   - RAG (检索增强生成) 架构
   - 实际案例: 企业知识库问答

3. **LangGraph: 图式编排** (25min)
   - 状态图 (StateGraph) 概念
   - 节点、边、条件路由
   - 人机协作 (Human-in-the-loop)
   - 检查点与持久化

4. **工作流设计模式** (20min)
   - 串行 vs 并行
   - Map-Reduce模式
   - 路由与分支
   - 错误处理与重试

**实验环节**: Lab 2 - 构建RAG工作流

---

### 📚 第5-6课时: 智能体架构：ReAct、反思、规划

**学习目标**:
- 理解Agent与工作流的本质区别
- 掌握主流Agent架构范式
- 学会评估Agent系统的可靠性

**内容大纲**:

1. **什么是Agent？** (15min)
   - 定义: 感知-决策-行动循环
   - Agent = LLM + Memory + Tools + Planning
   - 工作流是预定义的，Agent是自主的

2. **ReAct范式** (25min)
   - Reasoning + Acting
   - 思考链与行动交织
   - ReAct的局限性
   - 代码演示: 基础ReAct Agent

3. **反思机制 (Reflection)** (25min)
   - Self-Refine: 自我批评与改进
   - Reflexion: 经验积累
   - CRITIC: 外部工具验证
   - 案例: 代码Agent的自我debug

4. **规划能力 (Planning)** (25min)
   - Plan-and-Execute模式
   - Tree of Thoughts (ToT)
   - Graph of Thoughts (GoT)
   - 层级任务分解 (HTN)

**实验环节**: Lab 3 - 构建ReAct Agent

---

### 📚 第7-8课时: 记忆与工具：构建完整Agent

**学习目标**:
- 设计Agent的记忆系统
- 理解工具调用机制
- 掌握Skill/Plugin架构

**内容大纲**:

1. **Agent记忆系统** (25min)
   - 短期记忆: 对话上下文
   - 长期记忆: 向量数据库 + 摘要
   - 情景记忆 vs 语义记忆
   - MemGPT与自主记忆管理
   - 最新研究: MemR3自适应检索

2. **工具调用 (Tool Use)** (25min)
   - Function Calling机制
   - 工具描述的最佳实践
   - 并行工具调用
   - 工具编排与错误处理

3. **Skill与Plugin架构** (20min)
   - Skill: 可复用的能力单元
   - Plugin: 第三方扩展
   - 热加载与版本管理
   - OpenClaw的Skill体系

4. **Agent微调** (20min)
   - SFT: 监督微调基础
   - RLHF vs RLAIF
   - Agent专用数据集构建
   - LoRA/QLoRA高效微调

**实验环节**: Lab 3 (续) - 添加记忆和工具

---

## 第二天: 从多智能体到大模型操作系统

### 📚 第9-10课时: 多智能体协作与编排框架 

**学习目标**:
- 理解多智能体系统设计原则
- 掌握主流多智能体框架
- 学会选择合适的编排模式

**内容大纲**:

1. **多智能体系统概述** (20min)
   - 为什么需要多Agent？
   - 角色分工 vs 能力互补
   - 通信模式: 点对点、广播、黑板
   - 协调机制: 投票、辩论、层级

2. **AutoGen深度解析** (25min)
   - Microsoft的多Agent框架
   - 对话式协作模型
   - GroupChat与Manager
   - 案例: 多专家辩论系统

3. **CrewAI实战** (25min)
   - 角色定义 (Agent)
   - 任务分配 (Task)
   - 团队编排 (Crew)
   - 案例: 内容创作团队

4. **框架对比与选型** (20min)
   | 框架 | 特点 | 适用场景 |
   |------|------|----------|
   | LangGraph | 状态图、精细控制 | 企业级、合规要求高 |
   | CrewAI | 简洁直观、快速原型 | 创意工作流 |
   | AutoGen | 对话式、灵活 | 辩论、决策 |

**实验环节**: Lab 4 - 多智能体系统搭建

---

### 📚 第11-12课时: MCP协议与工具生态

**学习目标**:
- 深入理解MCP协议设计
- 掌握MCP Server开发
- 了解Agent互操作标准

**内容大纲**:

1. **MCP协议详解** (30min)
   - Model Context Protocol概述
   - 为什么Anthropic要推MCP？
   - 架构: Host、Client、Server
   - 传输层: stdio、HTTP/SSE
   - 核心能力: Resources、Tools、Prompts、Sampling

2. **MCP生态** (20min)
   - 官方SDK: TypeScript、Python
   - MCP Apps: UI能力扩展 (2026.01新)
   - 企业集成案例: Outreach、Salesforce
   - MCP Gateway: Obot等网关方案

3. **开发MCP Server** (25min)
   - 代码演示: 简单MCP Server
   - 工具定义最佳实践
   - 认证与安全
   - 调试技巧

4. **其他Agent协议** (15min)
   - OpenAI Plugins (已淘汰)
   - Semantic Kernel Skills
   - A2A (Agent-to-Agent) Protocol
   - 协议统一趋势

**实验环节**: Lab 4 (续) - 开发简单MCP Server

---

### 📚 第13-14课时: 大模型操作系统与前沿系统

**学习目标**:
- 理解"LLM OS"愿景
- 掌握前沿Agent系统
- 学会评估和选用Agent平台

**内容大纲**:

1. **LLM OS愿景** (20min)
   - Karpathy的LLM OS概念
   - 内核 = LLM
   - 文件系统 = 上下文窗口 + 记忆
   - 进程 = Agent
   - 系统调用 = 工具

2. **OpenClaw深度解析** (25min)
   - 架构: Gateway → Session → Agent
   - Skill系统与热加载
   - 多Channel支持 (飞书/TG/微信)
   - 多模态: 浏览器控制、Camera、Screen
   - Node网络与远程执行

3. **编码智能体对比** (25min)
   | 系统 | 模型 | 特点 | 最新Benchmark |
   |------|------|------|---------------|
   | Codex | GPT-5.3 | 终端原生、云沙箱 | Terminal-Bench 77.3% |
   | Claude Code | Claude 4.6 Opus | Git原生、大仓库 | 复杂debug优势 |
   | Cursor | 多模型 | IDE集成 | 交互式开发 |
   | Manus | 自研 | 全自动任务 | 综合Agent |

4. **多模态Agent** (20min)
   - Computer Use: 屏幕操作
   - Seedance 2.0: 视频生成Agent
   - 机器人Agent: 具身智能
   - 未来: 通用Agent

**现场演示**: OpenClaw实操、Claude Code对比Codex

---

### 📚 第15-16课时: 商业应用与未来展望

**学习目标**:
- 分析Agent的商业化路径
- 识别投资机会与风险
- 展望技术发展方向

**内容大纲**:

1. **Agent商业化现状** (25min)
   - 2025年AI风投: 2110亿美元
   - Agent创业赛道分类:
     - 垂直Agent (法律、医疗、金融)
     - 水平平台 (开发者工具、企业中台)
     - 基础设施 (评估、安全、编排)
   - 案例: Cursor ($4B)、Anthropic ($350B估值)

2. **行业应用深度剖析** (25min)
   - **软件开发**: Codex、Claude Code、Devin
   - **客户服务**: 对话Agent、工单自动化
   - **内容创作**: 写作、视频、营销
   - **数据分析**: BI Agent、自动报表
   - **运营自动化**: RPA + Agent

3. **Agent安全与治理** (20min)
   - 对齐问题 (Alignment)
   - 权限控制与沙箱
   - 审计与可解释性
   - 幻觉与事实核查
   - Red Team与Adversarial Testing

4. **2026-2030展望** (20min)
   - 技术趋势:
     - Reasoning Model持续突破
     - 多模态统一 (文本+图像+视频+音频+动作)
     - Agent间协议标准化
     - 本地/边缘Agent兴起
   - 产业趋势:
     - Agent即服务 (AaaS)
     - 人形机器人爆发 (Figure, Tesla, Unitree)
     - 知识工作自动化加速

**课程总结与Q&A**

---

## 📊 评估方式

| 组成部分 | 权重 | 说明 |
|----------|------|------|
| 出勤 | 10% | 课堂参与、讨论、提问 |
| Assignment 1 | 40% | 安装使用OpenClaw，完成使用报告 |
| Assignment 2 | 50% | Agent未来前瞻性调研报告，明确提出一个创业机会 |

**说明**:
- Labs为选修实验环节，不计入成绩
- Assignment 1要求亲手部署OpenClaw并体验核心功能
- Assignment 2需分析技术演进、商业模式、组织社会影响

### Assignment 1: OpenClaw使用报告 (40%)

**目标**: 通过实际安装和使用AI Agent系统，理解Agent的工作原理和能力边界

**要求**:
- 完成OpenClaw安装与配置
- 至少10轮以上对话体验
- 修改SOUL.md观察行为变化
- 使用至少3个内置Skill
- 提交使用报告（包含截图、体验反思、改进建议）

**截止**: 第二周上课前

### Assignment 2: Agent前瞻性调研报告 (50%)

**目标**: 深入研究Agent技术的未来演化路径，培养战略洞察力

**要求**:
报告需要涵盖以下三个维度：

1. **技术演化** (约30%)
   - Agent架构的发展趋势
   - 人机协作范式的演变
   - 关键技术突破点预测

2. **商业演化** (约30%)
   - 垂直行业应用前景
   - 商业模式创新
   - 市场规模预测

3. **组织/社会演化** (约30%)
   - 对就业市场的影响
   - 组织结构变革
   - 伦理与治理挑战

4. **创业机会** (约10%)
   - 提出一个明确的创业机会
   - 包含：问题定义、解决方案、目标市场、竞争分析、初步商业模式

**格式**: Markdown或PDF

**截止**: 课程结束后两周

---

## 📞 联系方式

- **授课教师**: 温颖，温睦宁
- **助教**: 王雅娟

---

*Version 1.0 | 2026-02-26*
