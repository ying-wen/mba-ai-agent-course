# LLM Post-Training 方法最新进展

> 课程参考材料 - L1-2大语言模型基础

## Post-Training方法演进

| 年份 | 主流方法 | 代表模型 | 特点 |
|------|----------|----------|------|
| 2022-2023 | RLHF (PPO) | ChatGPT, Claude 1-2 | 需要Reward Model + PPO |
| 2024 | DPO | Llama 3, Qwen 2 | 简化流程，无需RM |
| 2025 | GRPO | DeepSeek R1 | 适合推理任务，可验证奖励 |
| 2026 | RLAIF, GSPO, SCPO | Claude 4, Kimi K2, Qwen 3 | AI反馈+自我优化 |

## 方法对比

| 方法 | 需要RM | 复杂度 | 最适合场景 |
|------|--------|--------|-----------|
| RLHF | ✅ | 高 | 通用对话 |
| DPO | ❌ | 中 | 快速迭代 |
| GRPO | ❌ | 中 | 推理/数学 |
| RLAIF | ❌ | 中 | 大规模训练 |

## 商业含义

1. **GRPO让推理能力民主化** - DeepSeek突破证明
2. **RLAIF降低数据标注成本** - 不再依赖大量人工
3. **小团队也能做对齐训练** - 门槛持续下降

## 参考链接

- [PyTorch: A Primer on LLM Post-Training](https://pytorch.org/blog/a-primer-on-llm-post-training/)
- [HuggingFace: Guide to RL Post-Training](https://huggingface.co/blog/karina-zadorozhny/guide-to-llm-post-training-algorithms)
