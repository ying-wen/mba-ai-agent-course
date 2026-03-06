# L7-8 讲义：记忆系统与工具编排（完整版）

> **课程**: MBA大模型智能体课程  
> **课时**: 第7-8讲（90分钟）  
> **适用**: 讲师备课 / 学生预习与复习  
> **对应Slides**: `slides-marp/day1-lesson7-8-memory-tools.md`
> **参考资源**: Datawhale Hello-Agents 第八章：记忆与检索
> **最后更新**: 2026-03-06

---

## 本讲核心问题

1. **为什么Agent需要记忆？** LLM的上下文窗口够用吗？
2. **记忆有哪些类型？** 短期/长期/情景/语义怎么区分？
3. **工具使用是什么？** Function Calling如何工作？
4. **长时间任务怎么管理？** 如何设计Agent Harness？

---

## Part 1：为什么需要记忆系统

### LLM的根本限制

即使是200K tokens的上下文窗口，也无法处理：
- 长期对话历史（几个月的交互）
- 大量背景知识（整个公司的文档）
- 学习到的经验（过去任务的教训）

### 类比理解

```
LLM的上下文窗口 = 人的"工作记忆"（正在想的事）
外部记忆系统 = 人的"长期记忆"（记住的事）
```

人能记住20年前的事，但不能同时想1000件事。Agent也一样——需要外部存储来扩展记忆容量。

### LLM的两个根本性局限

#### 局限一：无状态导致的对话遗忘

当前的大语言模型虽然强大，但设计上是**无状态的**。每一次API调用都是独立的计算，这带来了几个问题：

1. **上下文丢失**：早期重要信息可能因窗口限制而丢失
2. **个性化缺失**：无法记住用户偏好、习惯或特定需求
3. **学习能力受限**：无法从过往的成功或失败中学习改进
4. **一致性问题**：多轮对话中可能前后矛盾

```python
# 无记忆Agent的问题演示
agent = SimpleAgent(name="学习助手", llm=llm)

# 第一次对话
response1 = agent.run("我叫张三，正在学习Python")
# "很好！Python基础语法是编程的重要基础..."

# 第二次对话（新会话）
response2 = agent.run("你还记得我的学习进度吗？")
# "抱歉，我不知道您的学习进度..."  ← 完全遗忘！
```

#### 局限二：模型内置知识的局限性

LLM的知识是**静态的、有限的**，完全来自训练数据：

1. **知识时效性**：训练数据有截止点，无法获取最新信息
2. **专业领域知识**：通用模型在特定领域深度不足
3. **事实准确性**：通过检索验证，减少幻觉问题
4. **可解释性**：提供信息来源，增强可信度

→ 这正是**RAG（检索增强生成）**技术应运而生的原因。

---

## Part 2：认知科学视角的记忆系统设计

### 2.1 人类记忆系统的层次结构

在构建智能体的记忆系统之前，我们需要从认知科学的角度理解人类是如何处理和存储信息的。

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        人类记忆系统的层次结构                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   外部刺激 → [感觉记忆] → [工作记忆] → [长期记忆]                         │
│              (0.5-3秒)    (15-30秒)    (终生)                            │
│                 ↓            ↓           ↓                              │
│              容量巨大      7±2项目    容量无限                           │
│              全感官        当前任务    永久存储                           │
│                                         ↓                               │
│                              ┌─────────┴─────────┐                      │
│                              ↓                   ↓                      │
│                         [程序性记忆]        [陈述性记忆]                 │
│                         技能和习惯          可言说的知识                  │
│                         (骑自行车)              ↓                        │
│                                      ┌─────────┴─────────┐              │
│                                      ↓                   ↓              │
│                                 [语义记忆]          [情景记忆]           │
│                                 一般知识            个人经历              │
│                                 (巴黎是首都)        (昨天会议)           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 三层记忆的认知科学解释

| 记忆层次 | 持续时间 | 容量 | 功能 | Agent映射 |
|---------|---------|------|------|----------|
| **感觉记忆** | 0.5-3秒 | 巨大 | 暂存原始感官信息 | 多模态输入缓冲 |
| **工作记忆** | 15-30秒 | 7±2项目 | 当前任务处理 | Prompt上下文 |
| **长期记忆** | 终生 | 近乎无限 | 永久存储 | 向量DB/知识图谱 |

### 2.3 程序性记忆 vs 陈述性记忆

| 维度 | 程序性记忆 | 陈述性记忆 |
|------|-----------|-----------|
| **定义** | 技能和习惯的记忆 | 可以用语言表达的知识 |
| **特点** | 自动化、难以言说 | 可意识提取、可言说 |
| **例子** | 骑自行车、打字、游泳 | 历史事件、数学公式 |
| **Agent映射** | 工具调用模式、固定流程 | 知识库、对话历史 |

### 2.4 语义记忆 vs 情景记忆

| 维度 | 语义记忆 | 情景记忆 |
|------|---------|---------|
| **内容** | 一般知识、概念、规则 | 个人经历、具体事件 |
| **时间性** | 不依赖特定时间 | 与特定时间地点绑定 |
| **例子** | "巴黎是法国首都" | "去年我去巴黎旅游" |
| **Agent存储** | 知识图谱、向量数据库 | 时间序列日志、会话记录 |
| **Agent检索** | 语义相似度检索 | 时间+语义混合检索 |

### 2.5 从人类记忆到Agent记忆的映射

```
┌────────────────────────────────────────────────────────────────────┐
│              人类记忆 → Agent记忆 映射关系                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  人类记忆类型          Agent实现              技术组件              │
│  ─────────────────────────────────────────────────────────────     │
│  感觉记忆              感知记忆              多模态编码器           │
│  (Sensory)            (PerceptualMemory)    CLIP/CLAP模型          │
│                                                                    │
│  工作记忆              工作记忆              内存列表 + TTL          │
│  (Working)            (WorkingMemory)       TF-IDF + 关键词        │
│                                                                    │
│  情景记忆              情景记忆              SQLite + Qdrant        │
│  (Episodic)           (EpisodicMemory)      时间序列 + 向量检索     │
│                                                                    │
│  语义记忆              语义记忆              Neo4j + Qdrant         │
│  (Semantic)           (SemanticMemory)      知识图谱 + 向量检索     │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## Part 3：记忆类型详解

### 3.1 四种记忆类型

```
┌─────────────────────────────────────────────────────┐
│                   Agent 记忆体系                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  工作记忆 (Working Memory)                         │
│  └── 当前对话的上下文                              │
│      特点: 容量有限(50条)、TTL自动清理             │
│      实现: 纯内存 + TF-IDF检索                     │
│                                                     │
│  情景记忆 (Episodic Memory)                        │
│  └── 过去执行任务的完整记录                        │
│      特点: 时间序列、会话级索引                    │
│      实现: SQLite + Qdrant向量检索                 │
│                                                     │
│  语义记忆 (Semantic Memory)                        │
│  └── 提取的事实、规则、知识                        │
│      特点: 实体关系、知识图谱                      │
│      实现: Neo4j图数据库 + Qdrant                  │
│                                                     │
│  感知记忆 (Perceptual Memory)                      │
│  └── 多模态数据（图像、音频等）                    │
│      特点: 跨模态检索、模态分离存储                │
│      实现: CLIP/CLAP编码 + Qdrant                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 3.2 各类型详细对比

| 类型 | 内容 | 存储周期 | 存储后端 | 检索方式 | 评分公式 |
|------|------|----------|---------|---------|---------|
| 工作记忆 | 当前对话 | 会话内 | 纯内存 | TF-IDF+关键词 | `(相似度×时间衰减)×(0.8+重要性×0.4)` |
| 情景记忆 | 任务记录 | 永久 | SQLite+Qdrant | 时间+向量 | `(向量×0.8+时间×0.2)×重要性权重` |
| 语义记忆 | 知识事实 | 永久 | Neo4j+Qdrant | 向量+图遍历 | `(向量×0.7+图×0.3)×重要性权重` |
| 感知记忆 | 多模态 | 动态 | Qdrant | 同/跨模态向量 | `(向量×0.8+时间×0.2)×重要性权重` |

---

## Part 4：HelloAgents 记忆系统架构

### 4.1 四层架构设计

```
┌─────────────────────────────────────────────────────────────────────┐
│                    HelloAgents 记忆系统架构                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 基础设施层 (Infrastructure Layer)                              │ │
│  │  ├── MemoryManager    - 记忆管理器（统一调度和协调）           │ │
│  │  ├── MemoryItem       - 记忆数据结构（标准化记忆项）           │ │
│  │  ├── MemoryConfig     - 配置管理（系统参数设置）               │ │
│  │  └── BaseMemory       - 记忆基类（通用接口定义）               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                              ↓                                      │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 记忆类型层 (Memory Types Layer)                                │ │
│  │  ├── WorkingMemory    - 工作记忆（临时信息，TTL管理）          │ │
│  │  ├── EpisodicMemory   - 情景记忆（具体事件，时间序列）         │ │
│  │  ├── SemanticMemory   - 语义记忆（抽象知识，图谱关系）         │ │
│  │  └── PerceptualMemory - 感知记忆（多模态数据）                 │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                              ↓                                      │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 存储后端层 (Storage Backend Layer)                             │ │
│  │  ├── QdrantVectorStore    - 向量存储（高性能语义检索）         │ │
│  │  ├── Neo4jGraphStore      - 图存储（知识图谱管理）             │ │
│  │  └── SQLiteDocumentStore  - 文档存储（结构化持久化）           │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                              ↓                                      │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 嵌入服务层 (Embedding Service Layer)                           │ │
│  │  ├── DashScopeEmbedding        - 通义千问嵌入（云端API）       │ │
│  │  ├── LocalTransformerEmbedding - 本地嵌入（离线部署）          │ │
│  │  └── TFIDFEmbedding            - TFIDF嵌入（轻量级兜底）       │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 快速体验：30秒上手记忆功能

```python
from hello_agents import SimpleAgent, HelloAgentsLLM, ToolRegistry
from hello_agents.tools import MemoryTool

# 创建具有记忆能力的Agent
llm = HelloAgentsLLM()
agent = SimpleAgent(name="记忆助手", llm=llm)

# 创建记忆工具
memory_tool = MemoryTool(user_id="user123")
tool_registry = ToolRegistry()
tool_registry.register_tool(memory_tool)
agent.tool_registry = tool_registry

# 添加记忆
memory_tool.execute("add", 
    content="用户张三是一名Python开发者",
    memory_type="semantic",
    importance=0.8
)

# 搜索记忆
result = memory_tool.execute("search", query="Python开发者", limit=5)
print(result)
```

---

## Part 5：MemoryTool 完整操作详解

### 5.1 操作总览

| 操作 | 功能 | 核心参数 |
|-----|------|---------|
| `add` | 添加记忆 | content, memory_type, importance |
| `search` | 搜索记忆 | query, limit, memory_types |
| `forget` | 遗忘记忆 | strategy, threshold, max_age_days |
| `consolidate` | 记忆整合 | from_type, to_type, importance_threshold |
| `summary` | 记忆摘要 | - |
| `stats` | 统计信息 | - |

### 5.2 add - 添加记忆（四种类型）

```python
# 1. 工作记忆 - 临时信息，会话结束后清理
memory_tool.execute("add",
    content="用户刚才问了关于Python函数的问题",
    memory_type="working",
    importance=0.6
)

# 2. 情景记忆 - 具体事件，包含时间地点
memory_tool.execute("add",
    content="2024年3月15日，用户张三完成了第一个Python项目",
    memory_type="episodic",
    importance=0.8,
    event_type="milestone"
)

# 3. 语义记忆 - 抽象知识，用于推理
memory_tool.execute("add",
    content="Python是一种解释型、面向对象的编程语言",
    memory_type="semantic",
    importance=0.9
)

# 4. 感知记忆 - 多模态信息
memory_tool.execute("add",
    content="用户上传了一张Python代码截图",
    memory_type="perceptual",
    modality="image",
    file_path="./uploads/code.png"
)
```

### 5.3 search - 搜索记忆（语义搜索）

```python
# 基础搜索
result = memory_tool.execute("search", query="Python编程", limit=5)

# 指定类型搜索
result = memory_tool.execute("search",
    query="学习进度",
    memory_type="episodic",
    limit=3
)

# 多类型搜索 + 重要性过滤
result = memory_tool.execute("search",
    query="函数定义",
    memory_types=["semantic", "episodic"],
    min_importance=0.5
)
```

### 5.4 forget - 遗忘机制（三种策略）

| 策略 | 说明 | 示例 |
|-----|------|-----|
| `importance_based` | 删除重要性低于阈值的记忆 | `threshold=0.2` |
| `time_based` | 删除超过指定天数的记忆 | `max_age_days=30` |
| `capacity_based` | 容量超限时删除最不重要的 | `threshold=0.3` |

```python
# 策略1: 基于重要性
memory_tool.execute("forget", strategy="importance_based", threshold=0.2)

# 策略2: 基于时间
memory_tool.execute("forget", strategy="time_based", max_age_days=30)

# 策略3: 基于容量
memory_tool.execute("forget", strategy="capacity_based", threshold=0.3)
```

### 5.5 consolidate - 记忆整合（短期→长期）

```
记忆整合路径:
工作记忆 ──(重要性≥0.7)──→ 情景记忆 ──(重要性≥0.8)──→ 语义记忆
  (临时)                    (长期事件)                  (抽象知识)
```

```python
# 将重要的工作记忆转为情景记忆
memory_tool.execute("consolidate",
    from_type="working",
    to_type="episodic",
    importance_threshold=0.7
)

# 将重要的情景记忆提炼为语义记忆
memory_tool.execute("consolidate",
    from_type="episodic",
    to_type="semantic",
    importance_threshold=0.8
)
```

---

## Part 6：存储后端详解

### 6.1 三种存储对比

| 存储类型 | 代表产品 | 特点 | 适用场景 |
|---------|---------|------|---------|
| **向量存储** | Qdrant | 高性能语义检索 | 语义相似度、多模态 |
| **图存储** | Neo4j | 关系推理、路径查询 | 知识图谱、实体关系 |
| **文档存储** | SQLite | 结构化查询、轻量级 | 元数据、会话历史 |

### 6.2 向量存储（Qdrant）

```bash
# 配置
QDRANT_URL=https://your-cluster.qdrant.tech:6333
QDRANT_API_KEY=your_api_key
QDRANT_COLLECTION=hello_agents_vectors
```

**适用**: 语义相似度检索、情景记忆向量索引、感知记忆多模态存储

### 6.3 图存储（Neo4j）

```bash
# 配置
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

**适用**: 实体关系存储、知识图谱构建、关系路径查询

### 6.4 文档存储（SQLite）

```sql
CREATE TABLE memories (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    memory_type TEXT NOT NULL,
    importance REAL DEFAULT 0.5,
    timestamp TEXT NOT NULL,
    metadata JSON
);
```

**适用**: 记忆元数据、会话历史、结构化查询

### 6.5 存储选择建议

| 部署环境 | 推荐配置 |
|---------|---------|
| 开发/测试 | SQLite + TFIDF |
| 生产-单机 | SQLite + Qdrant(云) + 本地Embedding |
| 生产-分布式 | Qdrant(云) + Neo4j(云) + DashScope |
| 边缘/离线 | SQLite + 本地Embedding |

---

## Part 7：嵌入服务配置

### 7.1 三种嵌入方案

| 方案 | 特点 | 适用场景 |
|-----|------|---------|
| **DashScope** | 云端API，中文优化 | 生产环境，中文场景 |
| **Local** | 离线运行，数据不出本地 | 隐私敏感，边缘部署 |
| **TFIDF** | 零依赖，纯Python | 快速原型，资源受限 |

### 7.2 配置示例

```bash
# DashScope（阿里云）
EMBED_MODEL_TYPE=dashscope
EMBED_MODEL_NAME=text-embedding-v3
EMBED_API_KEY=your_dashscope_api_key

# 本地模型
EMBED_MODEL_TYPE=local
EMBED_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

# TFIDF兜底
EMBED_MODEL_TYPE=tfidf
```

### 7.3 嵌入服务选择决策树

```
需要中文语义理解？
  ├─ 是 → 数据可上云？
  │       ├─ 是 → DashScope
  │       └─ 否 → 本地 (text2vec-base-chinese)
  │
  └─ 否 → 资源充足？
          ├─ 是 → 本地 (all-MiniLM-L6-v2)
          └─ 否 → TFIDF
```

---

## Part 8：MemGPT架构

### 创新点

MemGPT（2023）提出了一个类比操作系统的记忆管理方案：

```
传统方法:
[固定大小的上下文窗口，满了就截断]

MemGPT:
┌──────────────────────────────────────────────┐
│  Main Context (主上下文 - 类似内存)           │
│  • 系统提示词                                 │
│  • 当前对话                                   │
│  • 工作记忆                                   │
└────────────────────┬─────────────────────────┘
                     │
         LLM自主决定何时存入/读取
                     │
┌────────────────────┴─────────────────────────┐
│  External Storage (外部存储 - 类似硬盘)       │
│  • 历史对话摘要                               │
│  • 用户档案                                   │
│  • 长期记忆                                   │
└──────────────────────────────────────────────┘
```

### 核心创新

LLM自己决定何时"翻页"——读取/写入外部记忆，而不是程序员硬编码规则。

---

## Part 9：工具使用（Tool Use）

### Function Calling流程

```
1. 定义函数
   {
     "name": "get_weather",
     "description": "获取城市天气",
     "parameters": {
       "city": {"type": "string"}
     }
   }

2. 用户请求
   "上海今天天气怎么样？"

3. LLM生成函数调用
   {"name": "get_weather", "arguments": {"city": "上海"}}

4. 应用执行函数，返回结果
   {"temperature": 22, "condition": "晴"}

5. LLM根据结果生成回复
   "上海今天天气晴朗，气温22度，适合外出。"
```

### 常见工具类型

| 类型 | 示例 | 用途 |
|------|------|------|
| 搜索 | Google, Bing | 获取实时信息 |
| 计算 | 计算器, Python | 数学运算 |
| API | 天气、股票 | 特定领域数据 |
| 数据库 | SQL查询 | 结构化数据 |
| 文件 | 读写文件 | 文档处理 |
| 浏览器 | 网页操作 | Web交互 |

### 工具安全

| 风险 | 缓解措施 |
|------|----------|
| 注入攻击 | 输入验证、沙盒执行 |
| 权限滥用 | 最小权限原则 |
| 数据泄露 | 数据脱敏、访问控制 |
| 成本失控 | 调用次数限制 |

---

## Part 10：长时间运行Agent的Harness设计

### 来源

这部分内容来自Anthropic的工程实践文章：[Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

### 核心挑战

长时间运行的Agent（如需要几小时完成的开发任务）面临特殊挑战：
- 上下文会溢出
- 容易偏离方向
- 难以跟踪进度
- 失败后难以恢复

### 两部分架构

```
┌─────────────────────────────────────────────────────┐
│           长时间Agent架构                            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Part 1: Initializer Agent (初始化Agent)           │
│  ─────────────────────────────────────              │
│  • 理解用户意图                                     │
│  • 分解任务为feature_list.json                     │
│  • 快速执行，确保方向正确                          │
│                                                     │
│  Part 2: Coding Agent (执行Agent)                  │
│  ─────────────────────────────────                  │
│  • 按feature_list逐个实现                          │
│  • 更新claude-progress.txt                         │
│  • 每完成一项就测试验证                            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 常见失败模式与解决方案

| 失败模式 | 表现 | 解决方案 |
|----------|------|----------|
| **一次做太多** | 想同时改5个文件 | 强制每次只做一件事 |
| **过早宣布完成** | 说"完成了"但没测试 | 要求提供测试证据 |
| **偏离方向** | 做了没要求的功能 | 定期与feature_list核对 |
| **上下文丢失** | 忘了之前做了什么 | 读取progress文件 |
| **循环错误** | 反复犯同样的错 | 记录错误到blockers |

---

## Part 11：企业工具集成最佳实践

### 渐进式授权

```
阶段1: 只读权限
└── Agent只能查询，不能修改

阶段2: 受限写入
└── 低风险操作自动执行，高风险需要审批

阶段3: 完全授权
└── 建立信任后开放更多权限
```

### 审计日志

所有工具调用必须记录：
- 谁调用的
- 什么时间
- 调用什么工具
- 参数是什么
- 结果是什么

### 降级策略

工具不可用时的备选方案：

```
主方案: 调用内部API获取数据
   ↓ (失败)
备选1: 调用公开API
   ↓ (失败)
备选2: 搜索引擎获取
   ↓ (失败)
最终: 告知用户暂时无法获取
```

---

## 课堂实操

### 设计一个记忆系统（15分钟）

场景：客服Agent需要记住用户的历史咨询

设计要点：
1. 哪些信息存工作记忆？（当前对话上下文）
2. 哪些信息存情景记忆？（历史咨询记录）
3. 哪些信息存语义记忆？（用户画像、偏好）
4. 如何检索相关历史？（语义+时间混合检索）
5. 何时触发记忆整合？（重要性阈值）

---

## 本讲总结

### 核心概念

- **记忆系统**：扩展Agent的"记忆容量"
- **四种记忆类型**：工作/情景/语义/感知
- **三种存储后端**：向量(Qdrant)/图(Neo4j)/文档(SQLite)
- **Function Calling**：让LLM调用外部工具
- **Agent Harness**：管理长时间运行任务的框架

### 设计原则

1. **最小权限**：工具只开放必要的能力
2. **增量执行**：大任务分解为小步骤
3. **记录一切**：便于审计和恢复
4. **测试验证**：不是"说完成"而是"证明完成"

### 最佳实践速查

| 场景 | 推荐记忆类型 | 推荐存储 |
|-----|-------------|---------|
| 当前对话上下文 | WorkingMemory | 内存 |
| 用户历史行为 | EpisodicMemory | SQLite+Qdrant |
| 领域知识库 | SemanticMemory | Neo4j+Qdrant |
| 上传的图片/文件 | PerceptualMemory | Qdrant |

| 操作 | 建议阈值 |
|-----|---------|
| 整合(working→episodic) | 0.7 |
| 整合(episodic→semantic) | 0.8 |
| 遗忘(importance_based) | 0.2 |
| 搜索(min_importance) | 0.1 |

---

## 延伸阅读

### 论文
- [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)
- [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)

### 文章
- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

### 教程
- [Datawhale Hello-Agents 第八章：记忆与检索](https://github.com/datawhalechina/hello-agents)

---

*本讲义最后更新：2026-03-06*
*整合来源：Datawhale Hello-Agents 第八章*
