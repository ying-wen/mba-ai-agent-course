# Lab 2: 构建RAG工作流

## 🎯 学习目标

通过本实验，你将：
- 理解RAG (检索增强生成) 的完整流程
- 掌握文档分块、向量化、检索的实现
- 构建一个企业知识库问答系统

## 📋 环境准备

```bash
pip install langchain langchain-openai chromadb pypdf
```

## 📋 实验任务

### 任务1: 实现基础RAG流程

#### 1.1 文档加载与分块

```python
# rag_demo.py

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. 加载PDF文档
loader = PyPDFLoader("your_document.pdf")
documents = loader.load()

print(f"加载了 {len(documents)} 页文档")

# 2. 文本分块
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # 每块1000字符
    chunk_overlap=200,    # 块之间重叠200字符
    length_function=len,
    separators=["\n\n", "\n", "。", "，", " ", ""]
)

chunks = text_splitter.split_documents(documents)
print(f"分割成 {len(chunks)} 个文本块")

# 查看第一个块
print("第一个文本块内容:")
print(chunks[0].page_content[:500])
```

#### 1.2 向量化存储

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 3. 创建向量存储
embeddings = OpenAIEmbeddings()

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"  # 持久化存储
)

print("向量存储创建完成")

# 测试检索
query = "公司的主要业务是什么？"
results = vectorstore.similarity_search(query, k=3)

print(f"\n查询: {query}")
print("检索到的相关文档:")
for i, doc in enumerate(results):
    print(f"\n--- 文档 {i+1} ---")
    print(doc.page_content[:300])
```

#### 1.3 构建RAG链

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 4. 创建RAG链
llm = ChatOpenAI(model="gpt-4", temperature=0)

# RAG提示词模板
rag_prompt = ChatPromptTemplate.from_template("""
基于以下参考文档回答问题。如果文档中没有相关信息，请明确说明"根据提供的文档，我无法找到相关信息"。

参考文档:
{context}

问题: {question}

请用中文回答，并在适当时引用文档中的具体内容。
""")

# 创建检索器
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# 格式化检索结果
def format_docs(docs):
    return "\n\n".join([
        f"[文档{i+1}] {doc.page_content}" 
        for i, doc in enumerate(docs)
    ])

# 构建RAG链
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# 5. 测试问答
questions = [
    "公司去年的营收是多少？",
    "主要的产品线有哪些？",
    "未来的发展战略是什么？"
]

for q in questions:
    print(f"\n问: {q}")
    answer = rag_chain.invoke(q)
    print(f"答: {answer}")
```

### 任务2: 添加对话历史

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# 带记忆的RAG
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

conversational_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    verbose=True
)

# 多轮对话测试
def chat(question):
    result = conversational_chain.invoke({"question": question})
    print(f"\n问: {question}")
    print(f"答: {result['answer']}")
    print(f"\n参考来源: {len(result['source_documents'])} 个文档")
    return result

# 测试多轮对话
chat("公司的主营业务是什么？")
chat("那它的竞争对手有哪些？")  # 这里的"它"应该能理解为上文提到的公司
chat("相比竞争对手，有什么优势？")
```

### 任务3: 来源引用

```python
# 添加来源引用功能
def rag_with_sources(question):
    # 检索
    docs = retriever.invoke(question)
    
    # 构建带来源的上下文
    context_with_sources = ""
    sources = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "未知来源")
        page = doc.metadata.get("page", "未知页码")
        sources.append(f"{source} (第{page}页)")
        context_with_sources += f"\n[来源{i+1}: {source}, 第{page}页]\n{doc.page_content}\n"
    
    # 回答
    prompt = f"""
基于以下参考文档回答问题，并在回答中标注信息来源（使用[来源X]格式）。

参考文档:
{context_with_sources}

问题: {question}

请用中文回答，并标注每个关键信息的来源。
"""
    
    response = llm.invoke(prompt)
    
    return {
        "answer": response.content,
        "sources": sources
    }

# 测试
result = rag_with_sources("公司的财务状况如何？")
print("回答:", result["answer"])
print("\n引用来源:")
for s in result["sources"]:
    print(f"  - {s}")
```

## 📊 提交要求

1. 完整的`rag_demo.py`代码
2. 运行截图（展示问答效果）
3. 实验报告：
   - 分块策略的选择理由
   - 检索效果的评估
   - 遇到的问题和解决方法

## 💡 进阶挑战

- 尝试不同的chunk_size和chunk_overlap
- 比较不同的检索方法（similarity vs mmr）
- 添加"我不知道"的优雅处理

## 🔗 参考资源

- [LangChain RAG教程](https://python.langchain.com/docs/tutorials/rag/)
- [Chroma文档](https://docs.trychroma.com/)
