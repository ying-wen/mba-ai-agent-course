# Lab 3: 构建ReAct Agent

## 🎯 学习目标

通过本实验，你将：
- 理解ReAct (Reasoning + Acting) 范式
- 实现一个具备工具调用能力的Agent
- 添加Self-Refine反思机制

## 📋 环境准备

```bash
pip install langchain langchain-openai tavily-python
```

## 📋 实验任务

### 任务1: 实现基础ReAct Agent

```python
# react_agent.py

from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain.tools import Tool
import json

# 1. 定义工具
def search_web(query: str) -> str:
    """搜索网络获取信息"""
    # 实际应用中使用Tavily或其他搜索API
    # 这里用模拟数据演示
    mock_results = {
        "特斯拉市值": "特斯拉(TSLA)当前市值约1.2万亿美元，是全球最大的电动车制造商。",
        "苹果营收": "苹果2025财年营收达到4000亿美元，同比增长8%。",
        "英伟达": "英伟达2025年收入突破1000亿美元，AI芯片需求强劲。"
    }
    for key, value in mock_results.items():
        if key in query:
            return value
    return f"搜索结果: 关于'{query}'的最新信息..."

def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        # 安全的数学计算
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return "错误: 只支持基本数学运算"
        result = eval(expression)
        return f"计算结果: {expression} = {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"

def get_stock_price(ticker: str) -> str:
    """获取股票价格"""
    # 模拟数据
    prices = {
        "TSLA": {"price": 248.50, "change": "+2.3%"},
        "AAPL": {"price": 185.20, "change": "-0.5%"},
        "NVDA": {"price": 890.00, "change": "+3.1%"},
    }
    ticker = ticker.upper()
    if ticker in prices:
        data = prices[ticker]
        return f"{ticker} 当前价格: ${data['price']}, 涨跌: {data['change']}"
    return f"未找到股票 {ticker} 的数据"

# 创建工具列表
tools = [
    Tool(
        name="search",
        func=search_web,
        description="搜索网络获取最新信息。输入应该是搜索关键词。"
    ),
    Tool(
        name="calculator",
        func=calculate,
        description="计算数学表达式。输入应该是数学表达式，如 '100 * 1.2'"
    ),
    Tool(
        name="stock_price",
        func=get_stock_price,
        description="获取股票当前价格。输入应该是股票代码，如 'TSLA', 'AAPL'"
    )
]

# 2. 创建ReAct Agent
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 获取ReAct提示词模板
prompt = hub.pull("hwchase17/react")

# 创建Agent
agent = create_react_agent(llm, tools, prompt)

# 创建执行器
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # 显示详细的思考过程
    max_iterations=10,
    handle_parsing_errors=True
)

# 3. 测试Agent
def run_agent(question: str):
    print(f"\n{'='*50}")
    print(f"问题: {question}")
    print('='*50)
    result = agent_executor.invoke({"input": question})
    print(f"\n最终答案: {result['output']}")
    return result

# 测试用例
if __name__ == "__main__":
    # 简单查询
    run_agent("特斯拉的当前股价是多少？")
    
    # 需要计算
    run_agent("如果我有10000美元，按特斯拉当前股价能买多少股？")
    
    # 复杂推理
    run_agent("对比特斯拉和苹果的市值，哪个更大？差多少？")
```

### 任务2: 添加Self-Refine机制

```python
# self_refine_agent.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4", temperature=0)

def self_refine_agent(task: str, tools: list, max_iterations: int = 3):
    """带Self-Refine的Agent"""
    
    # 第一步: 初始执行
    print(f"\n[初始执行] 任务: {task}")
    initial_result = agent_executor.invoke({"input": task})
    current_answer = initial_result['output']
    print(f"[初始答案] {current_answer}")
    
    for i in range(max_iterations):
        # 第二步: 自我批评
        critique_prompt = ChatPromptTemplate.from_template("""
请严格评估以下回答的质量:

原始问题: {task}
当前回答: {answer}

请从以下角度评估:
1. 准确性: 信息是否正确？
2. 完整性: 是否完整回答了问题？
3. 逻辑性: 推理是否合理？

如果回答已经足够好，请回复"APPROVED"。
否则，详细说明需要改进的地方。
""")
        
        critique_chain = critique_prompt | llm
        critique = critique_chain.invoke({
            "task": task,
            "answer": current_answer
        }).content
        
        print(f"\n[自我批评 第{i+1}轮] {critique[:200]}...")
        
        # 检查是否通过
        if "APPROVED" in critique.upper():
            print("[通过] 答案已足够好")
            break
        
        # 第三步: 根据批评改进
        refine_prompt = ChatPromptTemplate.from_template("""
原始问题: {task}
当前回答: {answer}
批评意见: {critique}

请根据批评意见改进回答。如果需要，可以重新调用工具获取信息。
""")
        
        # 重新执行Agent，带上改进要求
        refined_task = f"""
原任务: {task}

之前的回答有以下问题需要改进:
{critique}

请重新回答，避免上述问题。
"""
        refined_result = agent_executor.invoke({"input": refined_task})
        current_answer = refined_result['output']
        print(f"\n[改进后答案] {current_answer}")
    
    return current_answer

# 测试
if __name__ == "__main__":
    result = self_refine_agent(
        "分析英伟达的投资价值，包括当前估值、增长潜力和主要风险",
        tools
    )
    print(f"\n{'='*50}")
    print(f"最终答案: {result}")
```

### 任务3: 添加记忆系统

```python
# agent_with_memory.py

from langchain.memory import ConversationBufferWindowMemory
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

class AgentWithMemory:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.tools = tools
        
        # 短期记忆: 最近5轮对话
        self.short_term_memory = ConversationBufferWindowMemory(
            k=5,
            memory_key="chat_history",
            return_messages=True
        )
        
        # 长期记忆: 向量存储
        self.embeddings = OpenAIEmbeddings()
        self.long_term_memory = Chroma(
            embedding_function=self.embeddings,
            persist_directory="./agent_memory"
        )
        
        # 创建Agent
        prompt = hub.pull("hwchase17/react-chat")
        self.agent = create_react_agent(self.llm, self.tools, prompt)
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.short_term_memory,
            verbose=True
        )
    
    def remember(self, text: str, metadata: dict = None):
        """保存到长期记忆"""
        self.long_term_memory.add_texts(
            texts=[text],
            metadatas=[metadata or {}]
        )
    
    def recall(self, query: str, k: int = 3) -> list:
        """从长期记忆检索"""
        results = self.long_term_memory.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
    
    def chat(self, message: str) -> str:
        """对话，并自动管理记忆"""
        # 检索相关长期记忆
        relevant_memories = self.recall(message)
        
        # 如果有相关记忆，添加到上下文
        if relevant_memories:
            memory_context = "\n".join([f"- {m}" for m in relevant_memories])
            enhanced_message = f"""
[相关历史信息]
{memory_context}

[当前问题]
{message}
"""
        else:
            enhanced_message = message
        
        # 执行Agent
        result = self.executor.invoke({"input": enhanced_message})
        answer = result['output']
        
        # 保存重要信息到长期记忆
        if any(keyword in message.lower() for keyword in ['记住', '我是', '我喜欢', '偏好']):
            self.remember(f"用户说: {message}")
        
        return answer

# 测试
if __name__ == "__main__":
    agent = AgentWithMemory()
    
    # 第一轮对话
    print(agent.chat("我是张三，我对科技股比较感兴趣"))
    
    # 第二轮对话 (测试短期记忆)
    print(agent.chat("基于我的偏好，推荐一只股票"))
    
    # 新会话 (测试长期记忆)
    agent2 = AgentWithMemory()
    print(agent2.chat("你还记得我的名字吗？"))
```

## 📊 提交要求

1. 完整的`react_agent.py`代码
2. 完整的`self_refine_agent.py`代码
3. 运行日志截图（展示Thought/Action/Observation循环）
4. 实验报告：
   - Agent在哪些场景表现好/不好？
   - Self-Refine带来了什么改进？
   - 你对Agent可靠性的思考

## 💡 进阶挑战

- 添加更多工具（如新闻API、财报API）
- 实现Reflexion机制（从失败中学习）
- 添加并行工具调用支持

## 🔗 参考资源

- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
