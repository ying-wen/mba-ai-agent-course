# L3-4 补充章节：RAG系统深度解析

> **课程**: MBA大模型智能体课程  
> **定位**: L3-4讲义的深度补充材料  
> **适用**: 需要深入理解RAG技术细节的学员  
> **建议**: 先完成主讲义学习，再阅读本补充材料

---

## Part A：RAG系统架构详解

### A.1 系统全景图

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         RAG系统完整架构                                      │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    离线阶段：索引构建 Pipeline                        │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │                                                                      │  │
│  │   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────────────┐  │  │
│  │   │ 文档加载 │───→│ 文档分块 │───→│ 向量嵌入 │───→│ 向量数据库存储  │  │  │
│  │   │ Loading │    │Chunking │    │Embedding│    │ Vector Store   │  │  │
│  │   └─────────┘    └─────────┘    └─────────┘    └─────────────────┘  │  │
│  │        │              │              │                   │          │  │
│  │   PDF/Word/      固定/语义/      OpenAI/       Pinecone/Milvus/    │  │
│  │   HTML/TXT       递归分块        BGE/GTE          Chroma           │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    在线阶段：检索生成 Pipeline                        │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │                                                                      │  │
│  │  ┌──────┐   ┌──────────┐   ┌──────┐   ┌──────────┐   ┌──────────┐  │  │
│  │  │ 用户 │──→│ 查询理解 │──→│ 检索 │──→│ 重排序   │──→│ 答案生成 │  │  │
│  │  │ 查询 │   │ Query    │   │Retrieve│  │ Rerank  │   │ Generate │  │  │
│  │  └──────┘   └──────────┘   └──────┘   └──────────┘   └──────────┘  │  │
│  │                  │              │           │              │        │  │
│  │            查询改写/        向量/稀疏/     Cross-        Prompt     │  │
│  │            意图识别         混合检索      Encoder        + LLM     │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### A.2 离线阶段：文档处理 Pipeline

#### Step 1：文档加载 (Document Loading)

不同格式的文档需要不同的解析器：

| 文档格式 | 解析工具 | 注意事项 |
|----------|----------|----------|
| **PDF** | PyPDF2, pdfplumber, Unstructured | 扫描件需OCR |
| **Word** | python-docx, mammoth | 保留格式信息 |
| **HTML** | BeautifulSoup, trafilatura | 清理标签噪声 |
| **Markdown** | 直接解析 | 保留结构 |
| **Excel/CSV** | pandas | 转换为自然语言描述 |

```python
# LangChain 文档加载示例
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredHTMLLoader
)

# 加载 PDF
loader = PyPDFLoader("company_handbook.pdf")
documents = loader.load()

# 每个 document 包含:
# - page_content: 文本内容
# - metadata: 来源、页码等元数据
```

#### Step 2：文档分块 (Chunking)

**详见 Part B**

#### Step 3：向量嵌入 (Embedding)

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# OpenAI Embedding
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# 开源替代: BGE-M3
embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs={'device': 'cuda'},
    encode_kwargs={'normalize_embeddings': True}
)

# 生成向量
vectors = embeddings.embed_documents([chunk.page_content for chunk in chunks])
```

#### Step 4：向量存储 (Vector Store)

```python
from langchain_community.vectorstores import Chroma, Milvus, Pinecone

# 使用 Chroma (本地开发)
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 使用 Pinecone (生产环境)
vectorstore = Pinecone.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name="my-index"
)
```

### A.3 在线阶段：检索生成 Pipeline

#### Step 1：查询理解

```python
# 查询改写示例
def rewrite_query(original_query: str) -> list[str]:
    """将用户查询改写为多个搜索友好的版本"""
    prompt = f"""
    原始问题: {original_query}
    
    请生成3个语义相似但表述不同的搜索查询，以提高召回率:
    """
    # 调用 LLM 生成改写
    return llm.generate(prompt)

# 示例
# 输入: "公司年假怎么算"
# 输出: ["年假计算方法", "带薪休假天数规定", "员工年假政策"]
```

#### Step 2：检索 (Retrieval)

**详见 Part C**

#### Step 3：重排序 (Reranking)

**详见 Part D**

#### Step 4：答案生成

```python
# RAG 生成 Prompt 模板
RAG_PROMPT = """
你是一个专业的问答助手。请基于以下参考内容回答用户问题。

## 参考内容
{context}

## 用户问题
{question}

## 回答要求
1. 仅基于参考内容回答，不要编造信息
2. 如果参考内容不足以回答问题，明确说明
3. 在适当位置引用来源

## 回答
"""
```

---

## Part B：Chunk策略详解

### B.1 为什么Chunk策略如此重要？

分块策略直接决定RAG的效果：

```
分块太大 (>2000 tokens)
├── 检索不精准：一个大块中只有一小部分相关
├── Token浪费：把很多无关内容塞给LLM
└── 成本增加：更多token = 更多费用

分块太小 (<100 tokens)
├── 上下文丢失：句子被截断，意义不完整
├── 检索困难：小块语义信息不够
└── 效率降低：需要检索更多块才能获得完整信息
```

### B.2 固定大小分块 (Fixed Size Chunking)

**原理**：按照固定字符数或token数切分

```python
from langchain.text_splitter import CharacterTextSplitter

splitter = CharacterTextSplitter(
    chunk_size=500,      # 每块500字符
    chunk_overlap=50,    # 重叠50字符
    separator="\n"       # 优先在换行处切分
)

chunks = splitter.split_documents(documents)
```

**优点**：
- 实现简单，速度快
- 每块大小一致，便于批处理
- 适合结构化程度低的文档

**缺点**：
- 可能在句子/段落中间切断
- 不考虑语义边界
- 重要信息可能被分割

**适用场景**：通用场景、快速原型

### B.3 递归分块 (Recursive Chunking)

**原理**：按照层级分隔符递归切分，优先保留语义完整性

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=[
        "\n\n",   # 首先按段落分
        "\n",     # 然后按行分
        "。",     # 然后按句子分（中文）
        ".",      # 英文句号
        " ",      # 最后按空格分
        ""        # 实在不行按字符分
    ]
)

chunks = splitter.split_documents(documents)
```

**优点**：
- 尽量保持语义完整性
- 自适应文档结构
- 平衡块大小和语义边界

**缺点**：
- 块大小不完全一致
- 对中文需要调整分隔符

**适用场景**：**推荐作为默认策略**

### B.4 语义分块 (Semantic Chunking)

**原理**：基于语义相似度决定切分点。当相邻句子的语义差异超过阈值时切分。

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

# 基于语义相似度分块
splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="percentile",  # 使用百分位数阈值
    breakpoint_threshold_amount=95           # 相似度低于95%时切分
)

chunks = splitter.split_documents(documents)
```

**工作原理**：
```
句子1: "公司成立于2010年，总部位于北京。"
句子2: "目前员工数量超过5000人。"
句子3: "下面介绍年假政策。"  ← 语义跳跃，在此切分
句子4: "正式员工每年享有15天年假。"
```

**优点**：
- 最好的语义完整性
- 自动识别主题边界
- 适合长文档

**缺点**：
- 需要调用Embedding，成本高
- 速度较慢
- 块大小变化大

**适用场景**：高质量要求、文档类型复杂

### B.5 重叠策略 (Overlap Strategy)

**为什么需要重叠？**

```
无重叠切分问题：
原文: "公司的年假政策规定，正式员工工作满一年后，可享受15天带薪年假。"
      ↓
Chunk 1: "公司的年假政策规定，正式员工工作满"
Chunk 2: "一年后，可享受15天带薪年假。"

问题: "工作满一年"被切断，Chunk 1和2单独都不完整
```

**重叠比例建议**：

| chunk_size | overlap | overlap比例 | 说明 |
|------------|---------|-------------|------|
| 500 | 50-100 | 10-20% | 常规选择 |
| 1000 | 100-200 | 10-20% | 长块可适当减少比例 |
| 200 | 40-60 | 20-30% | 短块需要更多重叠 |

### B.6 高级策略：父子分块 (Parent-Child Chunking)

**原理**：用小块检索，用大块生成

```
文档
├── 大块 (父块，用于LLM上下文)
│   ├── 小块1 (子块，用于检索)
│   ├── 小块2 (子块，用于检索)
│   └── 小块3 (子块，用于检索)
└── ...

检索时: 搜索小块，命中"小块2"
返回时: 返回"小块2"的父块，提供更完整的上下文
```

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

# 父块分割器 (大块)
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)

# 子块分割器 (小块)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

# 父文档存储
store = InMemoryStore()

# 创建检索器
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

# 检索时返回父块
docs = retriever.get_relevant_documents("年假政策")
```

### B.7 策略对比与选择建议

| 策略 | 语义完整性 | 速度 | 成本 | 推荐场景 |
|------|------------|------|------|----------|
| **固定大小** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | 快速原型、非关键场景 |
| **递归分块** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | **默认推荐** |
| **语义分块** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | 高质量要求 |
| **父子分块** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 长文档、需要上下文 |

**决策流程**：

```
开始
  │
  ├─ 快速原型/测试？ ──→ 固定大小 + 10%重叠
  │
  ├─ 生产环境？
  │   │
  │   ├─ 对精度要求极高？ ──→ 语义分块
  │   │
  │   ├─ 文档很长？ ──→ 父子分块
  │   │
  │   └─ 其他情况 ──→ 递归分块 + 15%重叠
  │
  └─ 持续迭代，根据效果调整参数
```

---

## Part C：检索策略详解

### C.1 Dense Retrieval（向量检索）

**原理**：将文本转换为稠密向量，通过向量相似度找到相关内容

```python
# Dense Retrieval 实现
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 1. 创建 Embedding 模型
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# 2. 创建向量存储
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 3. 向量检索
results = vectorstore.similarity_search(
    query="年假政策是什么？",
    k=5  # 返回最相似的5个
)
```

**工作原理**：
```
查询: "年假政策"
        ↓
    向量化: [0.12, -0.34, 0.56, ...]
        ↓
    相似度计算 (余弦相似度)
        ↓
    返回 Top-K 最相似的文档块
```

**优点**：
- 语义理解能力强
- 能找到同义词、近义词
- 适合自然语言查询

**缺点**：
- 对专有名词、数字、代码等精确匹配较弱
- 依赖Embedding模型质量
- 需要向量数据库支持

### C.2 Sparse Retrieval（稀疏检索 / BM25）

**原理**：基于词频统计的经典检索算法，关注关键词匹配

```python
from langchain_community.retrievers import BM25Retriever
from langchain.schema import Document

# 创建 BM25 检索器
bm25_retriever = BM25Retriever.from_documents(
    documents=chunks,
    k=5  # 返回前5个
)

# BM25 检索
results = bm25_retriever.get_relevant_documents("2024年Q3财报")
```

**BM25 公式核心思想**：
```
分数 = 词频(TF) × 逆文档频率(IDF)

- 词频：关键词在文档中出现越多，分数越高
- IDF：稀有词权重更高（"财报"比"的"重要）
```

**优点**：
- 精确匹配能力强
- 对专有名词、数字、代码效果好
- 速度快，不需要GPU
- 可解释性强

**缺点**：
- 不理解语义，"年假"和"休假"匹配不上
- 对拼写错误敏感
- 需要分词处理

### C.3 Hybrid Search（混合检索）

**原理**：结合Dense和Sparse的优势，取长补短

```python
from langchain.retrievers import EnsembleRetriever

# 创建两个检索器
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
bm25_retriever = BM25Retriever.from_documents(chunks, k=5)

# 创建混合检索器
ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.6, 0.4]  # 向量检索权重0.6，BM25权重0.4
)

# 混合检索
results = ensemble_retriever.get_relevant_documents("2024年Q3财报数据")
```

**融合策略**：

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| **加权求和** | score = w1*dense + w2*sparse | 简单有效 |
| **Reciprocal Rank Fusion (RRF)** | 基于排名融合，减少分数量纲影响 | **推荐** |
| **重排序后融合** | 先各自检索，再统一重排序 | 高质量要求 |

**RRF 公式**：
```
RRF_score(d) = Σ 1 / (k + rank_i(d))

k = 常数（通常60）
rank_i(d) = 文档d在第i个检索器中的排名
```

### C.4 检索策略对比

| 特性 | Dense (向量) | Sparse (BM25) | Hybrid (混合) |
|------|--------------|---------------|---------------|
| **语义理解** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **精确匹配** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **速度** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **专有名词** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **同义词** | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ |
| **复杂度** | 中 | 低 | 高 |

**选择建议**：

```
查询类型判断
     │
     ├─ 自然语言问题（"公司文化是什么"）
     │   └─ Dense 为主
     │
     ├─ 精确查询（"ISO9001证书编号"）
     │   └─ Sparse 为主
     │
     └─ 混合查询（"2024年Q3营收增长原因"）
         └─ Hybrid（推荐）
```

---

## Part D：重排序（Reranking）

### D.1 为什么需要重排序？

**问题**：初次检索（Retrieve）通常返回Top-K，但这些结果的相关性排序可能不准确

```
用户查询: "公司的年假政策是什么？"

初次检索返回 Top-5:
1. [相关度分数 0.89] 关于员工福利的概述... (不太相关)
2. [相关度分数 0.87] 年假申请流程说明... (部分相关)
3. [相关度分数 0.85] 正式员工年假天数规定... ← 最相关！
4. [相关度分数 0.84] 病假管理规定... (不相关)
5. [相关度分数 0.82] 考勤系统使用说明... (不相关)

问题: 最相关的内容排在第3位
```

**重排序的作用**：
```
重排序后:
1. [重排分数 0.95] 正式员工年假天数规定... ← 提升到第1位
2. [重排分数 0.78] 年假申请流程说明...
3. [重排分数 0.45] 关于员工福利的概述...
...
```

### D.2 Bi-encoder vs Cross-encoder

这是理解重排序的关键概念：

**Bi-encoder（双编码器）**：
```
查询 ──→ [Encoder A] ──→ Query向量 ──┐
                                      ├──→ 相似度计算
文档 ──→ [Encoder B] ──→ Doc向量  ──┘

特点:
- 查询和文档独立编码
- 可以预计算文档向量
- 速度快，但精度相对低
- 用于初次检索
```

**Cross-encoder（交叉编码器）**：
```
[查询, 文档] ──→ [Encoder] ──→ 相关性分数

特点:
- 查询和文档联合编码
- 每次都要重新计算
- 速度慢，但精度高
- 用于重排序
```

**对比**：

| 特性 | Bi-encoder | Cross-encoder |
|------|------------|---------------|
| **精度** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **速度** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **预计算** | ✅ 可以 | ❌ 不可以 |
| **用途** | 初次检索 | 重排序 |
| **处理量** | 百万级 | 百级 |

**实际流程**：
```
查询 → Bi-encoder检索 (快，处理百万文档) → Top-100
                ↓
        Cross-encoder重排序 (慢但准，只处理100个) → Top-5
                ↓
              LLM生成答案
```

### D.3 主流重排序工具

#### Cohere Rerank

```python
import cohere

co = cohere.Client("your-api-key")

# 重排序
results = co.rerank(
    query="年假政策是什么？",
    documents=[doc.page_content for doc in retrieved_docs],
    top_n=3,
    model="rerank-multilingual-v3.0"  # 多语言模型
)

# 结果
for result in results.results:
    print(f"排名: {result.index}, 分数: {result.relevance_score}")
```

**Cohere Rerank 特点**：
- 商业API，开箱即用
- 多语言支持优秀
- 性能业界领先
- 按调用次数计费

#### BGE-reranker（开源）

```python
from FlagEmbedding import FlagReranker

# 加载模型
reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)

# 计算相关性分数
pairs = [
    ["年假政策是什么？", doc.page_content] 
    for doc in retrieved_docs
]
scores = reranker.compute_score(pairs)

# 按分数排序
ranked_docs = sorted(
    zip(retrieved_docs, scores), 
    key=lambda x: x[1], 
    reverse=True
)
```

**BGE-reranker 特点**：
- 开源免费
- 中文效果好
- 支持多语言
- 需要GPU部署

#### 其他选择

| 工具 | 类型 | 特点 | 适用场景 |
|------|------|------|----------|
| **Cohere Rerank** | 商业API | 最强性能，易用 | 生产环境首选 |
| **BGE-reranker** | 开源 | 中文好，免费 | 自部署 |
| **Jina Reranker** | 商业+开源 | 长文本支持 | 长文档场景 |
| **ColBERT** | 开源 | 效率和精度平衡 | 大规模场景 |

### D.4 LangChain 集成示例

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

# 基础检索器
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

# 重排序器
compressor = CohereRerank(
    model="rerank-multilingual-v3.0",
    top_n=5
)

# 组合成压缩检索器
retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

# 检索 (自动重排序)
docs = retriever.get_relevant_documents("年假政策")
```

### D.5 重排序最佳实践

**1. 两阶段检索架构**：
```
阶段1: 粗排（Bi-encoder）
  - 从百万文档中检索 Top-100
  - 使用向量相似度
  
阶段2: 精排（Cross-encoder）
  - 从 Top-100 中重排序出 Top-5
  - 使用重排序模型
```

**2. K值选择**：

| 阶段 | K值建议 | 说明 |
|------|---------|------|
| 初次检索 | 20-100 | 确保召回 |
| 重排序后 | 3-5 | 精准上下文 |

**3. 成本考量**：
```
Cohere Rerank 定价参考:
- 每1000次搜索约 $2
- 每次搜索可包含多个文档

权衡: 重排序成本 vs 精度提升
```

---

## Part E：向量数据库选择

### E.1 主流向量数据库对比

| 数据库 | 类型 | 开源 | 部署方式 | 最佳场景 |
|--------|------|------|----------|----------|
| **Pinecone** | 托管云服务 | ❌ | SaaS | 快速上手，生产级 |
| **Milvus** | 分布式 | ✅ | 自部署/云 | 大规模，高性能 |
| **Qdrant** | 高性能 | ✅ | 自部署/云 | 平衡性能和易用 |
| **Chroma** | 轻量级 | ✅ | 嵌入式 | 原型，小规模 |
| **Weaviate** | 多模态 | ✅ | 自部署/云 | 图文混合 |
| **pgvector** | 扩展 | ✅ | PostgreSQL | 已有PG环境 |

### E.2 详细对比

#### Pinecone

```python
from pinecone import Pinecone, ServerlessSpec

# 初始化
pc = Pinecone(api_key="your-api-key")

# 创建索引
pc.create_index(
    name="my-index",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

# 使用
index = pc.Index("my-index")
index.upsert(vectors=[...])
results = index.query(vector=query_vector, top_k=10)
```

**优点**：
- 完全托管，零运维
- 性能稳定，SLA保证
- 生态完善（LangChain/LlamaIndex原生支持）
- 自动扩缩容

**缺点**：
- 成本较高
- 数据存在第三方
- 定制能力有限

**适用**：**快速上手、生产环境首选**

---

#### Milvus

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema

# 连接
connections.connect("default", host="localhost", port="19530")

# 创建 Collection
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535)
]
schema = CollectionSchema(fields, "my collection")
collection = Collection("my_collection", schema)

# 创建索引
collection.create_index(
    field_name="embedding",
    index_params={"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 1024}}
)
```

**优点**：
- 高性能（十亿级向量）
- 功能丰富（多种索引类型）
- 社区活跃
- Zilliz Cloud提供托管服务

**缺点**：
- 部署复杂
- 学习曲线陡峭
- 资源消耗大

**适用**：**大规模生产、性能要求高**

---

#### Qdrant

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# 初始化
client = QdrantClient(host="localhost", port=6333)

# 创建 Collection
client.create_collection(
    collection_name="my_collection",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# 插入
client.upsert(
    collection_name="my_collection",
    points=[
        PointStruct(id=1, vector=[0.1, 0.2, ...], payload={"text": "..."})
    ]
)

# 搜索
results = client.search(
    collection_name="my_collection",
    query_vector=[0.1, 0.2, ...],
    limit=10
)
```

**优点**：
- Rust实现，性能优秀
- API设计优雅
- 支持丰富的过滤条件
- 易于部署（单二进制）
- 有云服务

**缺点**：
- 规模上限不如Milvus
- 生态相对较新

**适用**：**中等规模、追求易用性**

---

#### Chroma

```python
import chromadb

# 初始化
client = chromadb.Client()

# 创建 Collection（自带embedding）
collection = client.create_collection(name="my_collection")

# 添加文档
collection.add(
    documents=["doc1", "doc2", "doc3"],
    metadatas=[{"source": "a"}, {"source": "b"}, {"source": "c"}],
    ids=["id1", "id2", "id3"]
)

# 查询
results = collection.query(
    query_texts=["年假政策"],
    n_results=2
)
```

**优点**：
- 极简API
- 嵌入式，无需服务
- 内置Embedding支持
- 适合快速原型

**缺点**：
- 不适合大规模
- 持久化能力弱
- 生产功能不完善

**适用**：**原型开发、小项目、学习**

---

#### Weaviate

```python
import weaviate

# 初始化
client = weaviate.Client("http://localhost:8080")

# 创建 Schema
class_obj = {
    "class": "Document",
    "vectorizer": "text2vec-openai",  # 自动向量化
    "properties": [
        {"name": "text", "dataType": ["text"]},
        {"name": "source", "dataType": ["string"]}
    ]
}
client.schema.create_class(class_obj)

# 添加数据（自动向量化）
client.data_object.create(
    {"text": "年假政策规定...", "source": "handbook.pdf"},
    "Document"
)
```

**优点**：
- 内置向量化模块
- 多模态支持（文本+图像）
- GraphQL API
- 模块化架构

**缺点**：
- 配置复杂
- 资源消耗大
- 学习成本高

**适用**：**多模态检索、复杂场景**

---

#### pgvector

```sql
-- 安装扩展
CREATE EXTENSION vector;

-- 创建表
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536)
);

-- 创建索引
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);

-- 插入
INSERT INTO documents (content, embedding) 
VALUES ('年假政策...', '[0.1, 0.2, ...]');

-- 查询
SELECT * FROM documents 
ORDER BY embedding <=> '[0.1, 0.2, ...]' 
LIMIT 5;
```

**优点**：
- 利用现有PostgreSQL
- SQL查询能力
- ACID事务支持
- 生态成熟

**缺点**：
- 性能不如专用向量数据库
- 大规模扩展困难

**适用**：**已有PostgreSQL、中小规模**

### E.3 选型决策矩阵

| 场景 | 推荐 | 备选 |
|------|------|------|
| **快速原型** | Chroma | - |
| **生产级SaaS** | Pinecone | Qdrant Cloud |
| **大规模自部署** | Milvus | Qdrant |
| **中等规模自部署** | Qdrant | Weaviate |
| **已有PostgreSQL** | pgvector | - |
| **多模态检索** | Weaviate | Pinecone |
| **预算敏感** | Qdrant/Milvus | pgvector |

### E.4 性能与成本速览

| 数据库 | 10M向量QPS | 启动成本(月) | 10M向量成本(月) |
|--------|------------|--------------|-----------------|
| **Pinecone** | 1000+ | $70 | $200+ |
| **Milvus** | 2000+ | 自部署 | 服务器成本 |
| **Qdrant** | 1500+ | 自部署/免费层 | $100+ |
| **Chroma** | 100 | 免费 | 免费 |
| **Weaviate** | 1000+ | 自部署 | 服务器成本 |
| **pgvector** | 500 | 已有PG | 已有PG |

*注：数字为估算参考，实际因配置而异*

---

## Part F：RAG评估

### F.1 为什么需要评估？

RAG系统有很多可调参数，如何知道改动是否有效？

```
改变分块大小 500→1000：效果变好了吗？
换用BGE-M3替代OpenAI：精度下降了多少？
增加重排序环节：值得额外的成本吗？
```

**没有评估 = 盲人摸象**

### F.2 RAG评估维度

```
┌─────────────────────────────────────────────────────────┐
│                     RAG 评估框架                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  检索质量评估                    生成质量评估            │
│  ─────────────                  ─────────────          │
│  • Context Precision            • Faithfulness         │
│  • Context Recall               • Answer Relevancy     │
│  • Context Relevancy            • Answer Correctness   │
│                                                         │
│  端到端评估                                              │
│  ─────────                                              │
│  • Answer Semantic Similarity                           │
│  • User Satisfaction (人工评估)                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### F.3 核心评估指标

#### Faithfulness（忠实度）

**定义**：生成的答案是否忠实于检索到的上下文？

```
上下文: "公司年假政策规定，正式员工每年享有15天带薪年假。"

问题: "年假有多少天？"

答案A: "正式员工每年有15天年假。" → Faithfulness = 1.0 ✓
答案B: "员工每年有20天年假。" → Faithfulness = 0.0 ✗ (幻觉)
```

**计算方法**：
```
1. 从答案中提取所有陈述(claims)
2. 检验每个陈述是否能从上下文中推断
3. Faithfulness = 可推断陈述数 / 总陈述数
```

#### Answer Relevancy（答案相关性）

**定义**：生成的答案与问题的相关程度

```
问题: "公司年假政策是什么？"

答案A: "正式员工每年享有15天带薪年假，入职满一年后生效。" 
       → Answer Relevancy = 0.95 ✓

答案B: "我们公司成立于2010年，总部在北京，是一家科技公司。"
       → Answer Relevancy = 0.1 ✗ (答非所问)
```

**计算方法**：
```
1. 根据答案生成多个可能的问题
2. 计算生成问题与原问题的语义相似度
3. Answer Relevancy = 平均相似度
```

#### Context Precision（上下文精确度）

**定义**：检索到的上下文中，相关内容排在前面的程度

```
检索返回5个文档块:
1. [相关] 年假天数规定
2. [不相关] 公司简介
3. [相关] 年假申请流程
4. [不相关] 考勤制度
5. [不相关] 办公用品申领

理想顺序: 相关的应该排在前面
Context Precision考量的是排序质量
```

#### Context Recall（上下文召回率）

**定义**：生成正确答案所需的信息，有多少被成功检索到？

```
正确答案需要的信息:
- 年假天数 (15天) ✓ 检索到了
- 生效条件 (满一年) ✓ 检索到了
- 申请流程 ✗ 没检索到

Context Recall = 2/3 = 0.67
```

### F.4 RAGAS框架

**RAGAS (Retrieval Augmented Generation Assessment)** 是最流行的RAG评估框架。

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from datasets import Dataset

# 准备评估数据
eval_data = {
    "question": ["公司年假政策是什么？", "如何申请年假？"],
    "answer": ["正式员工每年有15天年假...", "可以通过OA系统申请..."],
    "contexts": [
        ["年假规定：正式员工15天...", "申请流程..."],
        ["OA系统使用说明...", "审批流程..."]
    ],
    "ground_truth": ["正式员工每年享有15天带薪年假", "通过OA系统提交申请"]
}

dataset = Dataset.from_dict(eval_data)

# 运行评估
result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    ]
)

print(result)
# {
#     'faithfulness': 0.92,
#     'answer_relevancy': 0.88,
#     'context_precision': 0.75,
#     'context_recall': 0.80
# }
```

### F.5 构建评估数据集

**方法1：人工标注（推荐起步）**

```python
# 评估数据集模板
eval_dataset = [
    {
        "question": "公司的年假政策是什么？",
        "ground_truth": "正式员工每年享有15天带薪年假，入职满一年后生效。",
        "source_documents": ["handbook_ch3.pdf"]
    },
    {
        "question": "如何申请年假？",
        "ground_truth": "通过OA系统提交申请，需提前3天，经主管审批。",
        "source_documents": ["handbook_ch3.pdf", "oa_guide.pdf"]
    }
]
```

**方法2：LLM辅助生成**

```python
GENERATE_QA_PROMPT = """
基于以下文档内容，生成5对问答用于评估RAG系统。

文档内容:
{document}

要求:
1. 问题应该是用户可能真实询问的
2. 答案必须完全基于文档内容
3. 问题难度适中

输出JSON格式:
[
  {{"question": "...", "answer": "..."}}
]
"""
```

**方法3：生产日志分析**

```python
# 从真实用户问题中抽样
# 人工标注正确答案
# 持续积累评估集
```

### F.6 评估流程最佳实践

```
┌──────────────────────────────────────────────────────┐
│                RAG评估最佳实践流程                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│  1. 建立基线                                         │
│     • 准备50-100条评估数据                           │
│     • 跑一次完整评估，记录基线分数                   │
│                                                      │
│  2. 迭代优化                                         │
│     • 每次只改一个变量                               │
│     • 重新评估，对比分数变化                         │
│     • 记录实验日志                                   │
│                                                      │
│  3. A/B测试                                          │
│     • 生产环境小流量验证                             │
│     • 收集用户反馈                                   │
│                                                      │
│  4. 持续监控                                         │
│     • 定期评估                                       │
│     • 数据漂移检测                                   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### F.7 评估指标速查表

| 指标 | 评估什么 | 需要什么数据 | 理想值 |
|------|----------|--------------|--------|
| **Faithfulness** | LLM是否幻觉 | answer, context | >0.9 |
| **Answer Relevancy** | 答案是否切题 | question, answer | >0.85 |
| **Context Precision** | 检索排序质量 | context, ground_truth | >0.7 |
| **Context Recall** | 检索召回率 | context, ground_truth | >0.8 |

---

## 总结：RAG优化路线图

### 从0到1：快速搭建

```
文档 → RecursiveTextSplitter(500, 50) → OpenAI Embedding → Chroma → GPT-4
```

### 从1到10：基础优化

```
+ 调整chunk size (测试300/500/800)
+ 添加BM25混合检索
+ 添加Cohere Rerank
+ 迁移到Pinecone/Qdrant
```

### 从10到100：深度优化

```
+ 语义分块或父子分块
+ 查询改写/多路召回
+ 自建Embedding微调
+ RAGAS持续评估
```

### 优化优先级

```
通常ROI排序:
1. Chunk策略调优 ← 免费，效果显著
2. 添加重排序 ← 成本低，效果明显
3. 混合检索 ← 免费，效果中等
4. 向量数据库选型 ← 根据规模
5. Embedding模型优化 ← 高级优化
```

---

*本补充章节最后更新：2026-03-06*
