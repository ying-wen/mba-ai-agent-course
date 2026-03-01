# MBA LLM Agent课程 - 阅读清单

> 整理时间: 2026-02-28  
> 用途: 课前预习 / 课后深入 / 长期参考

---

## 🌟 核心必读 (Top 10)

### 1. 官方指南 (Industry Best Practices)

| 来源 | 标题 | 核心内容 | 对应课时 |
|------|------|----------|----------|
| **OpenAI** | [A Practical Guide to Building Agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) | 32页实战手册：Agent定义、三大组件、编排模式、Guardrails | L5-6 Agent |
| **Anthropic** | [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | 5大模式：Augmented LLM → Orchestrator-Workers | L5-6 Agent |
| **Anthropic** | [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) | RAG优化：1.9%失败率、49%成本降低 | L3-4 Workflow |
| **Anthropic** | [Demystifying Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Agent评估体系：Task/Trial/Grader、pass@k vs pass^k | L5-6 Agent |
| **Anthropic** | [Context Window Engineering](https://www.anthropic.com/engineering/context-window-engineering-for-agents) | Context Rot/Compaction/Note-taking | L7-8 Memory |
| **Anthropic** | [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) ⭐新增 | Initializer Agent、进度追踪、增量开发 | L7-8 Memory |

### 2. 经典技术博客

| 作者 | 标题 | 核心内容 | 对应课时 |
|------|------|----------|----------|
| **Lilian Weng** (OpenAI) | [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) | Agent公式：LLM + Memory + Planning + Tool Use | L5-6 Agent |
| **Chip Huyen** | [Building LLM Apps for Production](https://huyenchip.com/2023/04/11/llm-engineering.html) | 工程实践：prompt管理、成本优化 | L7-8 Memory |
| **Simon Willison** | [Agent Definition](https://simonw.substack.com/p/i-think-agent-may-finally-have-a) | "An LLM agent runs tools in a loop" | L5-6 Agent |
| **Manus Team** | [Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) ⭐新增 | 上下文工程的实验科学、4次架构重构经验 | L7-8 Memory |

### 3. 多Agent架构

| 来源 | 标题 | 核心内容 | 对应课时 |
|------|------|----------|----------|
| **LangChain** | [Choosing the Right Multi-Agent Architecture](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/) | 四种模式：subagents/skills/handoffs/routers | L9-10 Multi-Agent |
| **LangChain** | [Building LangGraph](https://blog.langchain.com/building-langgraph/) | Agent Runtime设计原则 | L9-10 Multi-Agent |
| **Anthropic** | [Multi-Agent Research System](https://www.anthropic.com/engineering/research-system) | 90.2%效果提升、CEO-Manager模式 | L9-10 Multi-Agent |

---

## 📚 按课时分类

### L1-2: LLM基础
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic Claude Documentation](https://docs.anthropic.com)

### L3-4: Workflow & RAG
- [Anthropic: Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
- [LangChain: RAG from Scratch](https://langchain-ai.github.io/langgraph/tutorials/rag/)

### L5-6: Agent
- [OpenAI: A Practical Guide to Building Agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) ⭐
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) ⭐
- [Anthropic: Demystifying Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Lilian Weng: LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) ⭐
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Reflexion Paper](https://arxiv.org/abs/2303.11366)
- [Tree of Thoughts Paper](https://arxiv.org/abs/2305.10601)

### L7-8: Memory & Tools
- [Anthropic: Context Window Engineering](https://www.anthropic.com/engineering/context-window-engineering-for-agents) ⭐
- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) ⭐新增
- [Manus: Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) ⭐新增
- [MemGPT Paper](https://arxiv.org/abs/2310.08560)
- [Toolformer Paper](https://arxiv.org/abs/2302.04761)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Lilian Weng: Agent Memory (MIPS)](https://lilianweng.github.io/posts/2023-06-23-agent/#component-two-memory)

### L9-10: Multi-Agent
- [LangChain: Choosing the Right Multi-Agent Architecture](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/) ⭐
- [LangChain: Benchmarking Multi-Agent Architectures](https://blog.langchain.com/benchmarking-multi-agent-architectures/)
- [Microsoft AutoGen](https://www.microsoft.com/en-us/research/project/autogen/)
- [CrewAI: Build Your First Crew](https://www.crewai.com/blog/build-your-first-crewai-agents)
- [Hugging Face: Transformers Agents 2.0](https://huggingface.co/blog/agents)

### L11-12: MCP & Tool Integration
- [MCP Official Documentation](https://modelcontextprotocol.io/introduction) ⭐
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [Anthropic: CLAUDE.md Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) ⭐
- [Simon Willison: LLM Tools](https://simonw.substack.com/p/large-language-models-can-run-tools)
- [ClawHub: Skills Marketplace](https://clawhub.com)
- [Smithery: MCP Server Directory](https://smithery.ai)

### L13-14: LLM OS & Advanced
- [Andrej Karpathy: Intro to LLMs (1h video)](https://youtube.com/watch?v=zjkBMFhNj_g) - LLM OS概念
- [Andrej Karpathy: Deep Dive into LLMs (3.5h video)](https://www.youtube.com/watch?v=7xTGNNLPyMI)
- [OpenClaw Documentation](https://docs.openclaw.ai) ⭐新增
- [Manus AI Architecture Paper](https://arxiv.org/html/2505.02024v1) ⭐新增

### L15-16: Business & Deployment
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Anthropic: Responsible Deployment](https://www.anthropic.com/news/responsible-scaling-policy)

---

## 🔬 前沿研究

### Google DeepMind
- [SIMA 2: Agent in 3D Worlds](https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/)
- [Gemini Robotics 1.5: Physical AI Agents](https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/)
- [Gemini 2.0: Agentic Era](https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/)

### 学术机构
- [BAIR Blog](https://bair.berkeley.edu/blog/)
- [Stanford AI Lab Blog](http://ai.stanford.edu/blog/)
- [The Gradient](https://thegradient.pub/)

---

## 🛠️ 前沿Agent框架与产品 ⭐新增章节

### 编码Agent

| 产品 | 厂商 | 特点 | 链接 |
|------|------|------|------|
| **Claude Code** | Anthropic | CLI Agent、CLAUDE.md、Thinking模式 | [GitHub](https://github.com/anthropics/claude-code) |
| **Codex** | OpenAI | Web+CLI双端、GitHub集成 | [官网](https://openai.com/codex) |
| **Devin** | Cognition | 全自主软件工程师、Devin Wiki | [官网](https://devin.ai) |

### AI IDE

| 产品 | 特点 | 链接 |
|------|------|------|
| **Cursor** | Composer、Background Agents、Plan Mode | [官网](https://cursor.com) |
| **Windsurf** | Cascade引擎、持久记忆 (前身Codeium) | [官网](https://windsurf.com) |

### 通用Agent框架

| 框架 | 开源 | 特点 | 链接 |
|------|------|------|------|
| **OpenClaw** | ✅ | 多渠道、MCP、Skills生态 | [Docs](https://docs.openclaw.ai) |
| **Manus** | ❌ | Context Engineering、已被Meta收购 | [官网](https://manus.im) |
| **LangGraph** | ✅ | Agent编排、状态图 | [Docs](https://langchain-ai.github.io/langgraph/) |
| **AutoGen** | ✅ | 多Agent对话 | [GitHub](https://github.com/microsoft/autogen) |
| **CrewAI** | ✅ | 团队协作Agent | [官网](https://www.crewai.com/) |

### 企业Agent

| 产品 | 厂商 | 特点 | 链接 |
|------|------|------|------|
| **Claude Cowork** | Anthropic | Office/Workspace集成、企业Plugins | [新闻](https://techcrunch.com/2026/02/24/anthropic-launches-new-push-for-enterprise-agents-with-plugins-for-finance-engineering-and-design/) |
| **Microsoft Copilot** | Microsoft | Office 365/Windows/GitHub集成 | [官网](https://copilot.microsoft.com/) |

### 低代码平台

| 平台 | 特点 | 链接 |
|------|------|------|
| **Dify** | 开源、工作流编排 | [官网](https://dify.ai/) |
| **Coze** | 字节跳动、插件生态 | [官网](https://www.coze.com/) |

---

## 📺 视频资源

| 作者 | 标题 | 时长 | 内容 |
|------|------|------|------|
| Andrej Karpathy | Intro to LLMs | 1h | LLM基础、LLM OS概念 |
| Andrej Karpathy | Deep Dive into LLMs | 3.5h | 训练全栈、Agent安全 |
| Yannic Kilcher | 论文解读系列 | varies | 最新论文讲解 |

---

## 📰 Newsletter & RSS

| 名称 | 频率 | 内容 |
|------|------|------|
| [Import AI](https://importai.substack.com/) | 周刊 | AI行业动态 |
| [The Batch](https://www.deeplearning.ai/the-batch/) | 周刊 | Andrew Ng主编 |
| [Alignment Forum](https://www.alignmentforum.org/) | 日更 | AI安全研究 |
| [LessWrong](https://www.lesswrong.com/) | 日更 | AI理性主义社区 |

---

## 🔐 安全与治理

- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OpenAI Model Spec](https://model-spec.openai.com/2025-12-18.html)
- [Anthropic Constitution](https://www.anthropic.com/index/claudes-constitution)
- [CrowdStrike: OpenClaw Security Analysis](https://www.crowdstrike.com/en-us/blog/what-security-teams-need-to-know-about-openclaw-ai-super-agent/) ⭐新增

---

_最后更新: 2026-02-28_
