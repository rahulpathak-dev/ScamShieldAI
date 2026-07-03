from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path

from app.ml.config import PROJECT_ROOT

try:
    from langchain_community.document_loaders import DirectoryLoader, TextLoader
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except Exception:  # pragma: no cover - optional assistant dependencies
    DirectoryLoader = None
    TextLoader = None
    HuggingFaceEmbeddings = None
    FAISS = None
    RecursiveCharacterTextSplitter = None

TOKEN_PATTERN = re.compile(r"[a-z0-9_]+")


@dataclass(frozen=True)
class RetrievedContext:
    content: str
    source: str
    score: float


class ScamKnowledgeRetriever:
    def __init__(self, knowledge_dir: str, vector_dir: str, embedding_model: str) -> None:
        self.knowledge_dir = self._resolve(knowledge_dir)
        self.vector_dir = self._resolve(vector_dir)
        self.embedding_model = embedding_model
        self._vector_store = None
        self._documents = self._load_plain_documents()
        self._load_vector_store()

    def retrieve(self, query: str, k: int = 4) -> list[RetrievedContext]:
        if self._vector_store is not None:
            docs = self._vector_store.similarity_search_with_score(query, k=k)
            return [
                RetrievedContext(
                    content=doc.page_content,
                    source=str(doc.metadata.get("source", "knowledge")),
                    score=float(score),
                )
                for doc, score in docs
            ]
        return self._lexical_retrieve(query, k=k)

    def build_index(self) -> int:
        if DirectoryLoader is None or HuggingFaceEmbeddings is None or FAISS is None or RecursiveCharacterTextSplitter is None:
            raise RuntimeError("LangChain, FAISS, and embedding dependencies are required to build the vector index.")
        loader = DirectoryLoader(
            str(self.knowledge_dir),
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120)
        chunks = splitter.split_documents(docs)
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        store = FAISS.from_documents(chunks, embeddings)
        self.vector_dir.mkdir(parents=True, exist_ok=True)
        store.save_local(str(self.vector_dir))
        self._vector_store = store
        return len(chunks)

    def _load_vector_store(self) -> None:
        if not self.vector_dir.exists() or HuggingFaceEmbeddings is None or FAISS is None:
            return
        try:
            embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
            self._vector_store = FAISS.load_local(str(self.vector_dir), embeddings, allow_dangerous_deserialization=True)
        except Exception:
            self._vector_store = None

    def _load_plain_documents(self) -> list[RetrievedContext]:
        if not self.knowledge_dir.exists():
            return []
        docs = []
        for path in self.knowledge_dir.rglob("*.md"):
            docs.append(RetrievedContext(content=path.read_text(encoding="utf-8"), source=str(path), score=0.0))
        return docs

    def _lexical_retrieve(self, query: str, k: int) -> list[RetrievedContext]:
        query_terms = set(TOKEN_PATTERN.findall(query.casefold()))
        scored = []
        for doc in self._documents:
            doc_terms = TOKEN_PATTERN.findall(doc.content.casefold())
            if not doc_terms:
                continue
            counts = {term: doc_terms.count(term) for term in query_terms}
            score = sum(counts.values()) / math.sqrt(len(doc_terms))
            if score > 0:
                scored.append(RetrievedContext(content=doc.content[:1400], source=doc.source, score=round(score, 4)))
        return sorted(scored, key=lambda item: item.score, reverse=True)[:k]

    def _resolve(self, value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else PROJECT_ROOT / path