#!/usr/bin/env python3
"""Lab 2 - 轻量级 RAG 工作流示例.

流程：文档加载 -> 分块 -> 向量化(TF-IDF) -> 检索 -> 基于证据回答
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DEFAULT_QUERY = "RAG为什么可以降低企业AI客服的幻觉风险？"
SAMPLE_DOCS = {
    "rag_basics.txt": """
RAG（Retrieval-Augmented Generation）是一种先检索、后生成的架构。
在传统大模型问答中，模型主要依赖参数记忆，容易在知识盲区产生幻觉。
RAG通过在回答前检索外部知识库（如政策文档、产品手册、FAQ），为生成提供证据。
这会提升可解释性和准确率，尤其适合企业场景。
""".strip(),
    "retail_case.md": """
零售企业案例：某连锁商超用AI客服回答会员积分、促销和物流问题。
上线初期，模型偶尔编造优惠规则，导致用户投诉。
改造后，系统先检索活动数据库和订单状态，再组织回答。
结果：错误答复率下降，人工转接率下降，用户满意度提升。
""".strip(),
    "evaluation_notes.md": """
RAG效果评估不仅看准确率，还要看业务指标：
1. 首次问题解决率（FCR）
2. 人工转接率
3. 用户投诉率
4. 平均处理时长（AHT）
此外，需要对知识库更新频率、索引刷新延迟做运维监控。
""".strip(),
}


@dataclass
class Chunk:
    chunk_id: str
    source: str
    text: str


class RAGWorkflow:
    def __init__(self, chunk_size: int = 120, overlap: int = 30) -> None:
        if overlap >= chunk_size:
            raise ValueError("overlap 必须小于 chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.vectorizer = TfidfVectorizer()
        self.chunks: list[Chunk] = []
        self.chunk_matrix = None

    def build_index(self, docs: list[tuple[str, str]]) -> None:
        self.chunks = self._chunk_documents(docs)
        if not self.chunks:
            raise ValueError("未能生成任何文本块，请检查文档内容")

        texts = [c.text for c in self.chunks]
        self.chunk_matrix = self.vectorizer.fit_transform(texts)

    def search(self, query: str, top_k: int = 3) -> list[tuple[Chunk, float]]:
        if self.chunk_matrix is None:
            raise RuntimeError("索引尚未构建，请先调用 build_index")

        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.chunk_matrix).flatten()

        k = min(top_k, len(self.chunks))
        idxs = np.argsort(scores)[::-1][:k]
        return [(self.chunks[i], float(scores[i])) for i in idxs]

    def answer(self, query: str, retrieved: list[tuple[Chunk, float]]) -> str:
        if not retrieved:
            return "未检索到相关信息，请尝试换一个问题。"

        contexts = [chunk.text for chunk, _ in retrieved]
        evidence = self._extract_sentences_by_overlap(query, contexts, max_sentences=4)

        if not evidence:
            evidence = [contexts[0][:160]]

        answer_lines = [
            "基于检索证据，结论如下：",
            "1) RAG通过在回答前检索企业可信知识，减少‘无依据生成’。",
            "2) 它将生成过程绑定到可追溯文档，能显著降低事实性幻觉。",
            "3) 在业务上，通常带来更低投诉率和更高首解率。",
            "",
            "证据片段：",
        ]
        answer_lines.extend([f"- {line}" for line in evidence])
        return "\n".join(answer_lines)

    def _chunk_documents(self, docs: list[tuple[str, str]]) -> list[Chunk]:
        all_chunks: list[Chunk] = []
        step = self.chunk_size - self.overlap

        for source, text in docs:
            words = text.split()
            if not words:
                continue

            chunk_count = 0
            for start in range(0, len(words), step):
                window = words[start : start + self.chunk_size]
                if not window:
                    break
                chunk_count += 1
                chunk_id = f"{source}#chunk_{chunk_count}"
                all_chunks.append(
                    Chunk(chunk_id=chunk_id, source=source, text=" ".join(window))
                )
                if start + self.chunk_size >= len(words):
                    break
        return all_chunks

    @staticmethod
    def _extract_sentences_by_overlap(
        query: str,
        contexts: Iterable[str],
        max_sentences: int = 4,
    ) -> list[str]:
        query_terms = {t for t in re.findall(r"[\w\u4e00-\u9fff]+", query.lower()) if len(t) > 1}
        candidates: list[tuple[int, str]] = []

        for context in contexts:
            sentences = re.split(r"(?<=[。！？.!?])\s*", context)
            for sent in sentences:
                sent = sent.strip()
                if not sent:
                    continue
                sent_terms = set(re.findall(r"[\w\u4e00-\u9fff]+", sent.lower()))
                overlap = len(query_terms & sent_terms)
                candidates.append((overlap, sent))

        ranked = sorted(candidates, key=lambda x: x[0], reverse=True)
        picked: list[str] = []
        for score, sent in ranked:
            if score <= 0 and picked:
                break
            if sent not in picked:
                picked.append(sent)
            if len(picked) >= max_sentences:
                break
        return picked


def ensure_sample_docs(data_dir: Path) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    existing = list(data_dir.glob("*.txt")) + list(data_dir.glob("*.md"))
    if existing:
        return

    for filename, content in SAMPLE_DOCS.items():
        (data_dir / filename).write_text(content, encoding="utf-8")


def load_documents(data_dir: Path) -> list[tuple[str, str]]:
    docs: list[tuple[str, str]] = []
    for path in sorted(data_dir.glob("*")):
        if path.suffix.lower() not in {".txt", ".md"}:
            continue
        text = path.read_text(encoding="utf-8").strip()
        if text:
            docs.append((path.name, text))
    return docs


def run_once(query: str, data_dir: Path, chunk_size: int, overlap: int, top_k: int) -> None:
    ensure_sample_docs(data_dir)
    docs = load_documents(data_dir)

    print(f"[1] 已加载文档: {len(docs)}")
    if not docs:
        print("未找到可用文档，请在 data/ 放入 .txt 或 .md 文件")
        return

    rag = RAGWorkflow(chunk_size=chunk_size, overlap=overlap)
    rag.build_index(docs)

    print(f"[2] 已生成文本块: {len(rag.chunks)}")
    results = rag.search(query, top_k=top_k)

    print(f"[3] Top-{len(results)} 检索结果:")
    for chunk, score in results:
        print(f"  - {chunk.chunk_id} (score={score:.3f})")

    print("\n[4] 最终回答:")
    print(rag.answer(query, results))


def interactive_loop(data_dir: Path, chunk_size: int, overlap: int, top_k: int) -> None:
    while True:
        query = input("\n请输入问题（exit退出）: ").strip()
        if query.lower() in {"exit", "quit", "q"}:
            print("已退出。")
            break
        if not query:
            continue
        run_once(query, data_dir, chunk_size, overlap, top_k)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lab2: RAG workflow demo")
    parser.add_argument("--query", default="", help="单次问答问题；为空时进入交互模式")
    parser.add_argument("--data-dir", default="data", help="文档目录（txt/md）")
    parser.add_argument("--chunk-size", type=int, default=120, help="每个chunk词数")
    parser.add_argument("--overlap", type=int, default=30, help="chunk重叠词数")
    parser.add_argument("--top-k", type=int, default=3, help="检索返回chunk数量")
    parser.add_argument("--demo-query", action="store_true", help="使用默认演示问题")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_dir = Path(args.data_dir)

    if args.demo_query and not args.query:
        args.query = DEFAULT_QUERY

    if args.query:
        run_once(args.query, data_dir, args.chunk_size, args.overlap, args.top_k)
    else:
        interactive_loop(data_dir, args.chunk_size, args.overlap, args.top_k)


if __name__ == "__main__":
    main()
