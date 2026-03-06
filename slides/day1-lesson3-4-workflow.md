---
marp: true
theme: default
paginate: true
backgroundColor: #f5f5f7
color: #1d1d1f
style: |
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');
  
  section {
    font-family: 'PingFang SC', 'Hiragino Sans GB', 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
    padding: 46px 64px;
    font-size: 30px;
    line-height: 1.38;
  }
  h1 { font-size: 1.65em; color: #0f172a; margin-bottom: 0.25em; }
  h2 { font-size: 1.28em; color: #334155; margin-bottom: 0.3em; }
  h3 { font-size: 1.05em; color: #475569; margin-bottom: 0.2em; }
  strong { color: #0b3ea8; }
  a { color: #0b57d0; text-decoration: underline; }
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
    font-size: 0.68em;
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
  }
  th {
    background: #dbeafe;
    color: #0f172a;
    border: 1px solid #bfdbfe;
    padding: 8px;
  }
  td {
    background: #ffffff;
    color: #334155;
    border: 1px solid #e2e8f0;
    padding: 8px;
  }
  blockquote {
    margin: 10px 0;
    padding: 10px 14px;
    border-left: 4px solid #2563eb;
    background: #eff6ff;
    color: #334155;
    border-radius: 0 8px 8px 0;
  }
  .muted { color: #64748b; font-size: 0.8em; }
  .kpi {
    display: inline-block;
    background: #e0f2fe;
    border: 1px solid #bae6fd;
    border-radius: 999px;
    padding: 4px 12px;
    margin-right: 8px;
    font-size: 0.62em;
    color: #0c4a6e;
  }
  .try {
    background: #ecfeff;
    border: 2px solid #06b6d4;
    border-radius: 12px;
    padding: 14px;
    margin-top: 12px;
  }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# 第3-4课时｜工作流与RAG
## MBA《大模型智能体》

**主题**：从"会聊天"到"会完成任务"
**时长**：90分钟（含动手）

---

# 今天你将掌握什么？

1. 为什么单次LLM调用在企业中不够用
2. 工作流三大模式：顺序、并行、条件分支
3. RAG原理：检索、向量化、分块、生成
4. 如何把工作流 + RAG落到真实业务
5. 如何评估效果、控制成本和风险

---

# 课程结构（90分钟）

| 模块 | 内容 | 时间 |
|---|---|---|
| A | 为什么需要工作流 | 15 min |
| B | 工作流三大模式 | 20 min |
| C | RAG原理与关键技术 | 30 min |
| D | 场景落地与实操 | 20 min |
| E | 总结与讨论 | 5 min |

---

# 先做一个判断题

> "只要Prompt写得好，复杂业务也能一次调用搞定。"

- A. 正确
- B. 错误

**答案**：B（大多数企业任务都需要多步骤编排）

---

# 单次调用的4个天然短板

| 短板 | 结果 |
|---|---|
| 上下文有限 | 长文档/多文档处理不完整 |
| 知识陈旧 | 无法回答最新事实 |
| 无状态执行 | 难以跟踪任务进度 |
| 缺乏动作能力 | 不能主动调用系统完成任务 |

---

# 短板1：上下文不是无限的

- 企业常见输入：合同包、财报合集、历史工单
- "塞不下" ≠ "理解不好"
- 即使上下文很大，也会带来：
  - 费用上升
  - 速度下降
  - 注意力稀释

> 结论：必须做任务分解与检索

---

# 短板2：模型不知道"你公司内部"的知识

- LLM预训练知识有截止日期
- 内部制度/产品手册/会议纪要不在公开语料
- 纯生成容易"看起来合理，但并不真实"

**RAG价值**：把"企业私有知识"接到模型上

---

# 短板3：复杂任务不是一句话

典型任务：
- "帮我写竞品分析并给出行动建议"

隐藏步骤至少包括：
1. 收集信息
2. 交叉验证
3. 结构化分析
4. 输出成特定格式
5. 人工复核

---

# 短板4：一步到位不利于风控

- 无法定位错误发生在哪一步
- 无法给出可审计的中间结果
- 无法设置"人工审批点"

**企业需要**：可追踪、可回溯、可治理

---

# 什么是工作流（Workflow）

**定义**：把复杂任务拆成多个可执行节点，并定义节点之间的依赖关系。

```text
输入 → 节点1(提取) → 节点2(分析) → 节点3(生成) → 输出
```

工作流强调：
- 流程确定性
- 中间产物可见
- 错误可恢复

---

# 工作流带来的商业价值

<span class="kpi">准确率↑</span><span class="kpi">一致性↑</span><span class="kpi">风险↓</span><span class="kpi">可维护性↑</span>

1. 结果更稳定：标准化流程
2. 团队可协作：节点职责清晰
3. 可持续优化：可替换单个节点
4. 可运营：可监控每一步成本与时延

---

# 工作流三大模式总览

| 模式 | 核心问题 | 典型用途 |
|---|---|---|
| 顺序（Pipeline） | 先做什么后做什么 | 文档处理链 |
| 并行（Parallel） | 哪些能同时做 | 多源分析 |
| 条件分支（Router） | 根据什么走不同路径 | 客服分流 |

---

# 模式一：顺序执行（Pipeline）

```text
用户输入
  ↓
信息抽取 → 事实核验 → 结论生成 → 格式化输出
```

适用于：
- 上下游强依赖
- 需要逐步精炼
- 每步都有明确输入输出

---

# 顺序模式的设计要点

1. 每个节点只做一件事（单一职责）
2. 中间结果结构化（JSON优先）
3. 为关键节点设置质量门槛
4. 失败节点支持重试和降级

---

# 顺序模式示例：研报生成

| 节点 | 输入 | 输出 |
|---|---|---|
| N1 数据收集 | 公司名 | 原始资料包 |
| N2 事实整理 | 资料包 | 结构化事实表 |
| N3 分析推理 | 事实表 | SWOT结论 |
| N4 报告成稿 | SWOT | Markdown/PPT摘要 |

---

# 顺序模式伪代码

```python
facts = extract(raw_docs)
checked_facts = verify(facts)
analysis = reason(checked_facts)
report = format_report(analysis)
return report
```

> 每一步都可单测，便于团队并行开发。

---

# 动手试试 1：Prompt链式执行

<div class="try">

**平台直达链接**：
- [DeepSeek Chat](https://chat.deepseek.com)
- [Kimi 智能助手](https://kimi.moonshot.cn)

**任务**：以"某上市公司"生成简报
1) 先提取事实 2) 再做SWOT 3) 最后生成500字摘要
对比"一次性让模型写完"与"链式执行"的质量差异。

</div>

---

# 模式二：并行执行（Parallel）

```text
            ┌→ 财务分析 ─┐
用户问题 ───┼→ 舆情分析 ─┼→ 汇总器 → 统一回答
            └→ 产品分析 ─┘
```

并行价值：
- 降低总耗时
- 增强覆盖面
- 避免单一视角偏差

---

# 并行模式适用场景

- 多来源搜索（新闻+财报+论坛）
- 多角色评审（法务+财务+业务）
- 多假设评估（乐观/中性/悲观）

注意：并行不是"把同一件事重复3遍"。

---

# 并行模式的两个核心问题

1. **结果冲突怎么处理？**
   - 置信度排序
   - 引用来源优先
2. **汇总器怎么写？**
   - 先归纳共同点
   - 再列出分歧与原因

---

# 并行模式伪代码

```python
a = analyze_finance(data)
b = analyze_market(data)
c = analyze_product(data)
final = merge([a, b, c], strategy="evidence_first")
return final
```

---

# 动手试试 2：多角度并行分析

<div class="try">

**平台直达链接**：
- [Kimi](https://kimi.moonshot.cn)
- [Gemini](https://gemini.google.com)

**任务**：问题"AI手机2026年的机会点是什么？"
请分别从：技术、渠道、用户、监管四个角度独立产出，再做统一汇总。

</div>

---

# 模式三：条件分支（Router）

```text
输入请求 → 意图识别
             ├─ 售后问题 → 售后流程
             ├─ 购买咨询 → 销售流程
             └─ 投诉升级 → 人工专席
```

核心：先分类，再执行不同流程。

---

# Router的关键：分类标准

- 标签要互斥且穷尽（MECE）
- 置信度阈值要明确
- 低置信度要走"兜底路径"

> 不确定时，宁可转人工，不要乱答。

---

# Router常见实现策略

| 策略 | 优点 | 风险 |
|---|---|---|
| 规则优先（关键词） | 稳定可控 | 覆盖有限 |
| LLM分类 | 灵活 | 一致性波动 |
| 混合策略 | 平衡稳定与灵活 | 系统更复杂 |

---

# Router伪代码

```python
intent, score = classify(user_query)
if score < 0.65:
    return handoff_to_human(user_query)
elif intent == "refund":
    return refund_workflow(user_query)
elif intent == "consult":
    return consult_workflow(user_query)
else:
    return complaint_workflow(user_query)
```

---

# 动手试试 3：做一个客服分流器

<div class="try">

**平台直达链接**：
- [OpenAI Playground](https://platform.openai.com/playground)
- [Claude](https://claude.ai)

**任务**：把用户消息分到`退款/咨询/投诉/其他`，并输出JSON：
`{"intent":...,"confidence":...,"reason":...}`

</div>

---

# 三种模式如何组合？

企业真实流程通常是：

```text
Router(先分流) → Parallel(并行取数) → Pipeline(串行成稿)
```

这就是"组合编排"思想。

---

# 工作流质量指标（业务视角）

| 指标 | 解释 |
|---|---|
| 成功率 | 任务最终完成比例 |
| 一次通过率 | 无需人工返工 |
| 平均耗时 | 从输入到输出 |
| 单任务成本 | API+算力+人工 |
| 可解释性 | 能否追踪证据链 |

---

# 工作流 vs Agent（再对比）

| 维度 | 工作流 | Agent |
|---|---|---|
| 决策路径 | 预定义 | 动态规划 |
| 可靠性 | 高 | 中 |
| 灵活性 | 中 | 高 |
| 治理成本 | 低 | 高 |

**MBA建议**：先工作流，后Agent增强。

---

# 什么场景先上Workflow，什么场景上Agent？

- **Workflow优先**：标准化流程、监管要求高、容错低
- **Agent优先**：探索性任务、开放目标、路径不确定
- **混合方案**：Agent做规划，Workflow做执行

---

# 低代码工作流平台：Coze

**Coze** 是字节跳动推出的AI Bot开发平台，提供可视化工作流编排。

| 特点 | 说明 |
|------|------|
| **可视化编排** | 拖拽式节点连接，无需代码 |
| **多模型支持** | 豆包、GPT、Claude等 |
| **插件生态** | 100+官方插件，支持自定义 |
| **一键发布** | 发布到飞书、微信、网页等 |
| **免费额度** | 个人用户可免费使用 |

入口：[coze.cn](https://www.coze.cn)（国内）/ [coze.com](https://www.coze.com)（海外）

---

# Coze 核心概念

| 概念 | 说明 | 类比 |
|------|------|------|
| **Bot** | 一个完整的AI应用 | 小程序 |
| **Workflow** | 可视化流程编排 | 流程图 |
| **Plugin** | 调用外部能力 | API接口 |
| **Knowledge** | 知识库（RAG） | 参考资料 |
| **Memory** | 对话记忆 | 聊天历史 |

---

# Coze Workflow 节点类型

| 节点类型 | 功能 | 使用场景 |
|----------|------|----------|
| **LLM** | 调用大模型 | 文本生成、分析 |
| **Code** | 运行代码 | 数据处理、计算 |
| **Knowledge** | 知识检索 | RAG问答 |
| **Plugin** | 调用插件 | 搜索、API调用 |
| **Condition** | 条件分支 | 流程控制 |
| **Loop** | 循环处理 | 批量任务 |
| **Variable** | 变量操作 | 数据存储 |

---

# Coze 案例1：智能客服Bot

**场景**：电商售后客服自动回复

**Workflow设计**：
```text
用户提问 → 意图识别(LLM) → 条件分支
                              ├─ 退换货 → 查订单(Plugin) → 生成回复
                              ├─ 物流查询 → 快递API(Plugin) → 生成回复
                              └─ 其他 → 知识库检索 → 生成回复
```

**效果**：
- 80%问题自动解决
- 响应时间 < 3秒
- 7×24小时服务

---

# Coze 案例2：日报生成助手

**场景**：每日自动生成行业资讯日报

**Workflow设计**：
```text
定时触发 → 搜索新闻(Plugin) → 并行处理
                              ├─ 科技新闻 → 摘要生成(LLM)
                              ├─ 财经新闻 → 摘要生成(LLM)
                              └─ 政策动态 → 摘要生成(LLM)
         → 汇总排版(LLM) → 发送飞书/邮件
```

**效果**：
- 每天6:00自动推送
- 覆盖50+信息源
- 节省2小时/天人工整理

---

# Coze 案例3：面试助手

**场景**：HR筛选简历+生成面试问题

**Workflow设计**：
```text
上传简历(PDF) → 解析提取(LLM) → 匹配JD(Knowledge)
             → 评分打分(LLM) → 条件分支
                              ├─ 高匹配 → 生成面试问题
                              └─ 低匹配 → 生成拒绝理由
```

**效果**：
- 简历筛选效率提升5倍
- 面试问题针对性强
- 减少主观偏见

---

# Coze 案例4：会议纪要助手

**场景**：会议录音自动生成纪要

**Workflow设计**：
```text
上传音频 → 语音转文字(Plugin) → 内容分段(LLM)
         → 并行处理
            ├─ 提取要点(LLM)
            ├─ 提取待办(LLM)
            └─ 提取决议(LLM)
         → 格式化输出(LLM) → 发送参会者
```

**效果**：
- 30分钟会议 → 2分钟出纪要
- 自动识别待办事项
- 支持多语言

---

# Coze 案例5：投研分析助手

**场景**：上市公司快速调研

**Workflow设计**：
```text
输入公司名 → 并行获取数据
              ├─ 财报数据(Plugin)
              ├─ 新闻舆情(Plugin)
              ├─ 行业报告(Knowledge)
              └─ 竞品信息(Plugin)
           → 综合分析(LLM) → 生成研报摘要
           → 风险提示(LLM) → 输出PDF
```

**效果**：
- 5分钟完成初步调研
- 数据来源可追溯
- 支持定期跟踪

---

# 动手试试：Coze快速上手

<div class="try">

**平台直达**：[coze.cn](https://www.coze.cn)

**10分钟任务**：
1. 注册账号，创建新Bot
2. 添加一个简单Workflow：`用户输入 → LLM处理 → 输出`
3. 测试对话效果
4. 尝试添加一个Plugin节点（如：搜索）

</div>

---

# 过渡：为什么要学RAG？

即使流程设计很好，如果知识来源不可靠，输出仍不可靠。

**RAG解决的问题**：
1. 给模型"可查证"的外部知识
2. 让回答基于证据而非记忆

---

# RAG一句话定义

**RAG = Retrieval + Generation**

- 检索（Retrieval）：找到最相关资料
- 生成（Generation）：基于资料组织回答

> 核心不是"更会写"，而是"更会找"。

---

# RAG与纯LLM的差异

| 方式 | 数据来源 | 可追溯性 | 幻觉风险 |
|---|---|---|---|
| 纯LLM | 参数记忆 | 弱 | 高 |
| RAG | 外部知识库 + 参数 | 强 | 低 |

---

# RAG总架构（两阶段）

```text
离线阶段：文档清洗 → 分块 → 向量化 → 建索引
在线阶段：问题向量化 → 检索TopK → 重排 → 生成回答
```

离线决定"搜得全不全"，在线决定"答得准不准"。

---

# 阶段1：离线索引（Indexing）

1. 文档采集：PDF、网页、表格、知识库
2. 文本清洗：去噪、去模板、补元数据
3. 分块：控制粒度与上下文完整性
4. 向量化：文本转Embedding
5. 存储：向量库 + 元数据索引

---

# 阶段2：在线检索（Retrieval）

1. Query理解与改写
2. 召回（Top-K）
3. 重排（Re-rank）
4. 组装上下文
5. 约束生成（含引用）

---

# 阶段3：生成（Grounded Generation）

好的RAG回答应该：
- 明确引用来源
- 对不确定信息说"不知道"
- 给出可验证证据片段

推荐提示词约束：
```text
若资料缺失，请明确说明"未在检索结果中找到证据"。
```

---

# 向量化（Embedding）是什么？

把文本映射到高维向量空间：

- 语义相近 → 距离近
- 语义不同 → 距离远

```text
"苹果是一种水果"  ↔  "香蕉是一种水果" （近）
"苹果是一种水果"  ↔  "债券收益率曲线" （远）
```

---

# 向量化直觉图（概念）

```text
水果簇:  苹果●  香蕉●  橙子●

汽车簇:  特斯拉● 宝马● 奔驰●
```

检索本质：找到与问题向量"最近"的若干文本块。

---

# Embedding模型怎么选？

| 模型 | 维度 | 特点 | 适用场景 |
|------|------|------|----------|
| OpenAI text-embedding-3-large | 3072 | 多语言强 | 通用场景 |
| BGE-M3 | 1024 | 中文优化，开源 | 中文场景 |
| Jina-embeddings-v3 | 1024 | 长文本支持 | 文档检索 |
| Cohere embed-v3 | 1024 | 多语言、企业级 | 企业应用 |
| GTE-Qwen2 | 1024 | 阿里开源，中文强 | 中文+代码 |

**选型关键维度**：语言覆盖、领域适配、向量维度、推理成本

---

# 相似度计算：常用指标

- 余弦相似度（Cosine）
- 点积（Dot Product）
- 欧氏距离（L2）

在工程中，余弦最常见；关键是与模型训练目标一致。

---

# 动手试试 4：看见"语义相似"

<div class="try">

**平台直达链接**：
- [Hugging Face Spaces](https://huggingface.co/spaces)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)

**任务**：输入3组句子，观察相似度分数，验证"语义相近并非词面相同"。

</div>

---

# 向量数据库在做什么？

向量数据库不只是"存向量"，还包括：
- 近似最近邻搜索（ANN）
- 元数据过滤（时间/部门/文档类型）
- 分片扩容与高并发查询

| 数据库 | 特点 | 适用场景 |
|--------|------|----------|
| Milvus | 分布式，高性能 | 大规模生产 |
| pgvector | PostgreSQL扩展 | 已有PG基础设施 |
| Qdrant | Rust实现，快速 | 中等规模 |
| Chroma | 轻量级 | 原型开发 |
| Pinecone | 全托管SaaS | 快速上线 |
| Weaviate | 语义搜索原生 | AI应用 |

---

# Top-K到底取多少？

- K太小：可能漏召回
- K太大：噪声多、成本高

实践建议（起步）：
- 召回`K=20`，重排后取`Top 5~8`进入生成

---

# 重排（Re-rank）为什么重要？

流程：
1. 粗召回（快）
2. 精重排（准）

收益：
- 显著提升最终答案质量
- 降低"看似相关但其实无关"的干扰

---

# 分块（Chunking）为什么关键？

分块是RAG效果的"地基"。

- 太大：召回粗糙
- 太小：语义断裂
- 无重叠：边界信息丢失

---

# 常见分块策略对比

| 策略 | 做法 | 适用场景 |
|---|---|---|
| 固定长度 | 每N字切分 | 快速起步 |
| 段落切分 | 按自然段/标题 | 文档结构清晰 |
| 语义切分 | 根据语义变化切 | 精度优先 |
| 混合切分 | 标题+长度+重叠 | 生产环境常用 |

---

# 块大小与重叠率经验值

建议起点：
- 中文：`300~800字/块`
- 重叠：`10%~20%`

根据任务调参：
- 问答偏事实：块可小一点
- 复杂推理：块可稍大

---

# 结构化文档的分块技巧

针对合同/财报/手册：
1. 先按章节标题切分
2. 保留层级路径（如`3.2.1`）
3. 块内附带元数据（页码、版本、日期）

元数据是后续引用与审计的关键。

---

# 动手试试 5：Chunk参数实验

<div class="try">

**平台直达链接**：
- [Dify](https://dify.ai)
- [Coze](https://www.coze.cn)

**任务**：同一文档尝试两组参数：
A: `chunk=300 overlap=30`
B: `chunk=800 overlap=120`
比较：召回相关性、回答完整性、延迟。

</div>

---

# Query改写：让"搜"更聪明

用户问题常常过短、过口语化。可先做：
- 关键词扩展
- 同义词补全
- 时间范围补充

示例：
`"这家公司最近怎么样"` → `"公司近12个月营收、利润、重大事件"`

---

# 混合检索：Dense + Sparse

- Dense（向量）：擅长语义相似
- Sparse（关键词/BM25）：擅长精确词匹配

混合检索可同时兼顾：
- 专有名词准确命中
- 语义相关扩展召回

---

# Anthropic: Contextual Retrieval

> 来源: [Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) (Anthropic, 2024)

**问题**：传统RAG分块会丢失上下文

```text
原始chunk: "The company's revenue grew by 3%..."
问题: 哪家公司？哪个季度？
```

**解决方案**：用LLM为每个chunk生成上下文前缀

```text
上下文化chunk: "This chunk is from ACME Corp's Q2 2023 
SEC filing. The company's revenue grew by 3%..."
```

---

# Contextual Retrieval 效果

| 方法 | Top-20检索失败率 |
|------|------------------|
| 传统RAG | 5.7% |
| + Contextual Embeddings | 3.7% (↓35%) |
| + Contextual BM25 | 2.9% (↓49%) |
| + Reranking | **1.9%** (↓67%) |

**实现成本**：借助Prompt Caching，约$1/百万token

---

# RAG常见失败模式

1. 检索不到（Recall不足）
2. 检索错了（Precision不足）
3. 生成胡说（未约束）
4. 来源冲突（未做证据对齐）
5. 过时文档（知识库未更新）

---

# 如何评估RAG效果？

| 维度 | 指标示例 |
|---|---|
| 检索层 | Recall@K, MRR, nDCG |
| 生成层 | Faithfulness, Answer Relevancy |
| 业务层 | 工单解决率、人工接管率 |

评估必须分层，不要只看"主观好不好"。

---

# 动手试试 6：搭一个迷你RAG Bot

<div class="try">

**平台直达链接**：
- [Dify Cloud](https://cloud.dify.ai)
- [Coze Studio](https://www.coze.cn/home)

**任务**：上传10页以内文档，配置知识库问答Bot，测试5个问题，记录：
1) 是否给出处 2) 是否回答超范围问题 3) 是否出现幻觉

</div>

---

# Workflow + RAG 怎么结合？

典型组合：

```text
Router → (RAG检索节点) → 分析节点 → 生成节点 → 审核节点
```

要点：RAG不是独立产品，而是工作流中的"知识供给模块"。

---

# 企业参考架构（简版）

| 层 | 能力 |
|---|---|
| 接入层 | Chat/API/企业IM |
| 编排层 | Workflow/Router/监控 |
| 知识层 | 文档库/向量库/元数据 |
| 模型层 | Embedding + LLM + Re-ranker |
| 治理层 | 权限、审计、评估、告警 |

---

# 应用场景1：智能客服

流程：
1. Router识别意图
2. RAG查找知识条款
3. 生成答复 + 来源
4. 低置信度转人工

收益：
- 首响速度提升
- 人工坐席压力下降
- 口径一致性提升

---

# 应用场景2：投研助理

- 并行拉取：财报、新闻、研报
- RAG保障事实依据
- 工作流生成：日报/周报/策略备忘

对管理层价值：
- 缩短信息到决策的链路

---

# 应用场景3：法务合同审查

- 按条款分块比对标准模板
- 检索历史风险案例
- 生成风险等级与修改建议

关键要求：
- 必须可追溯到条款片段
- 必须保留人工终审

---

# 应用场景4：员工知识助手

- 覆盖制度、流程、FAQ、SOP
- 回答附"文档页码 + 更新时间"
- 过期知识自动降权

这类场景通常ROI最快。

---

# 成本与时延怎么控？

1. 优先优化检索，减少无效上下文
2. 小模型做分类/改写，大模型做最终生成
3. 缓存高频问题
4. 分级服务（普通问答 vs 高价值问答）

---

# 安全与权限不可忽视

- 按用户身份做文档访问控制（RBAC）
- 敏感字段脱敏（手机号、身份证、合同金额）
- 全链路日志审计
- 避免把机密信息送到不合规模型

---

# 人在回路（Human in the Loop）

建议把人工审核放在：
- 高风险结论输出前
- 合同/财务/医疗等关键场景
- 低置信度分支

"全自动"不是目标，"可控自动化"才是目标。

---

# 从0到1实施路线图（第1个月）

1. 选一个高频低风险场景
2. 整理小规模高质量知识库
3. 搭建最小可用Workflow + RAG
4. 做A/B测试与人工评估

---

# 从1到10扩展路线图（季度）

- 增加场景覆盖（客服→法务→HR）
- 建立统一知识治理规范
- 建立评估看板与告警机制
- 推进组织培训与流程改造

---

# 常见反模式（Anti-pattern）

1. 一上来追求"全公司大一统平台"
2. 只看Demo，不看线上指标
3. 忽略知识更新机制
4. 不做权限隔离
5. 把Agent当"万能员工"

---

# MBA视角：你需要做的5个决策

1. 先切哪个场景？
2. KPI如何定义？
3. 谁负责知识治理？
4. 风险红线在哪里？
5. 如何平衡效率与合规？

---

# 小组讨论（8分钟）

请按小组回答：
1. 你们公司最适合先落地哪个场景？
2. 该场景的关键知识源是什么？
3. 哪个环节必须保留人工？
4. 预期3个月内能提升什么指标？

---

# 课堂练习任务卡

**任务**：设计一个"企业知识问答"最小流程图
输出要求：
- 至少包含`Router + RAG + 人工兜底`
- 给出3个关键指标
- 给出1个风险控制点

---

# 动手试试 7：可视化流程搭建

<div class="try">

**平台直达链接**：
- [Langflow](https://www.langflow.org)
- [Flowise](https://flowiseai.com)
- [n8n](https://n8n.io)

**任务**：画出并运行一个"查询→检索→回答→引用"的流程，截屏保存。

</div>

---

# 动手试试 8：评估你的RAG

<div class="try">

**平台直达链接**：
- [Ragas 文档](https://docs.ragas.io)
- [TruLens](https://www.trulens.org)

**任务**：对同一知识库构造10个测试问题，记录`准确性/引用充分性/幻觉率`。

</div>

---

# 本课重点回顾（1/2）

- 工作流让任务可拆解、可监控、可优化
- 三大模式是所有复杂编排的基础积木
- 企业落地先追求稳定，再追求自治

---

# 本课重点回顾（2/2）

- RAG本质是"把外部知识接入模型推理"
- 向量化决定"能否找到相关信息"
- 分块策略决定"检索质量上限"
- 评估与治理决定"能否规模化上线"

---

# 推荐阅读与工具清单

- [RAG论文：Lewis et al. 2020](https://arxiv.org/abs/2005.11401)
- [Self-RAG (Asai et al., 2023)](https://arxiv.org/abs/2310.11511)
- [RAPTOR (Sarthi et al., 2024)](https://arxiv.org/abs/2401.18059)
- [CRAG (Yan et al., 2024)](https://arxiv.org/abs/2401.15884)
- [Pinecone: Advanced RAG](https://www.pinecone.io/learn/advanced-rag/)
- [Anthropic: Contextual Retrieval（已验证）](https://www.anthropic.com/engineering/contextual-retrieval)
- [LlamaIndex 文档](https://docs.llamaindex.ai)
- [LangChain 文档](https://python.langchain.com)

---

# 课后作业（可选加分）

1. 选择一个你熟悉的业务场景
2. 画出Workflow流程图（至少6个节点）
3. 给出RAG知识源与分块方案
4. 提交1页"上线风险清单"

---

# 下一课预告

## 第5-6课时：Agent架构与工具调用

- Agent的规划、记忆、工具、反思
- 多智能体协作与失败恢复
- 企业级Agent治理框架

---

<!-- _class: lead -->
<!-- _backgroundColor: #0f172a -->
<!-- _color: #ffffff -->

# Q & A
## 谢谢大家

**你可以带走一句话：**
先把流程做对，再把智能做强。

