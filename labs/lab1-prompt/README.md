# Lab 1: Prompt Engineering Playground

## 🎯 学习目标

通过本实验，你将：
- 理解Zero-shot、Few-shot、Chain-of-Thought的区别
- 掌握角色设定和系统提示词的设计技巧
- 学会迭代优化Prompt

## 📋 实验任务

### 任务1: 对比三种Prompt技巧

使用同一个问题，对比三种方法的效果：

**测试问题**: "一家公司第一季度收入100万，第二季度增长20%，第三季度比第二季度下降10%，第四季度与第三季度持平。全年总收入是多少？"

#### 1.1 Zero-shot (直接提问)

```python
from openai import OpenAI

client = OpenAI()

# Zero-shot: 直接提问
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "一家公司第一季度收入100万，第二季度增长20%，第三季度比第二季度下降10%，第四季度与第三季度持平。全年总收入是多少？"}
    ]
)
print("Zero-shot结果:", response.choices[0].message.content)
```

#### 1.2 Few-shot (给出示例)

```python
# Few-shot: 先给例子
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": """示例1:
问: 小明有5个苹果，吃了2个，又买了3个，现在有几个？
答: 5 - 2 + 3 = 6个

示例2:
问: 一件商品原价100元，打8折后是多少？
答: 100 × 0.8 = 80元

现在请回答:
问: 一家公司第一季度收入100万，第二季度增长20%，第三季度比第二季度下降10%，第四季度与第三季度持平。全年总收入是多少？"""}
    ]
)
print("Few-shot结果:", response.choices[0].message.content)
```

#### 1.3 Chain-of-Thought (引导思考)

```python
# CoT: 引导逐步思考
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": """一家公司第一季度收入100万，第二季度增长20%，第三季度比第二季度下降10%，第四季度与第三季度持平。全年总收入是多少？

请一步一步计算，列出每个季度的收入，最后求和。"""}
    ]
)
print("CoT结果:", response.choices[0].message.content)
```

### 任务2: 角色设定实验

为你所在的行业设计一个"专家Prompt"。

**模板**:
```python
system_prompt = """
你是一位{角色定位}，具有以下特点：
- 专业背景：{背景描述}
- 工作经验：{经验年限}
- 专长领域：{专长列表}

你的回答风格：
1. {风格特点1}
2. {风格特点2}
3. {风格特点3}

回答格式要求：
- {格式要求1}
- {格式要求2}
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "你的测试问题"}
    ]
)
```

**示例 - 投资分析师**:
```python
system_prompt = """
你是一位资深投资分析师，具有以下特点：
- 专业背景：CFA持证人，曾任职于高盛、摩根士丹利
- 工作经验：15年买方研究经验
- 专长领域：科技行业、成长股估值、行业趋势预判

你的回答风格：
1. 数据驱动：每个观点都有数据支撑
2. 风险意识：总是指出潜在风险
3. 可操作：给出明确的投资建议

回答格式要求：
- 先给结论（Executive Summary）
- 再展开分析
- 最后给投资建议和目标价
"""
```

### 任务3: Prompt优化迭代

选择一个实际业务场景，通过3轮迭代优化Prompt。

**记录模板**:
```markdown
## 场景描述
[你要解决的问题]

## 第1轮
**Prompt**: 
[你的prompt]

**输出**: 
[模型输出]

**问题**: 
[输出中的问题]

## 第2轮
**改进点**: 
[你做了什么改进]

**Prompt**: 
[改进后的prompt]

**输出**: 
[模型输出]

**问题**: 
[还存在的问题]

## 第3轮
**改进点**: 
[你做了什么改进]

**Prompt**: 
[最终prompt]

**输出**: 
[模型输出]

**效果评估**: 
[最终效果如何]
```

## 📊 提交要求

1. 任务1的三种方法对比结果截图
2. 任务2的专家Prompt完整代码
3. 任务3的迭代记录文档
4. 总结：你学到了什么？

## 💡 提示

- Temperature=0 时输出更稳定，适合对比实验
- 复杂任务分解成多个简单步骤
- 给出明确的输出格式要求
- 迭代是Prompt工程的核心，不要期望一次完美

## 🔗 参考资源

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
