from app.core.config import get_settings
from app.assistant.rag import ScamKnowledgeRetriever


def main() -> None:
    settings = get_settings()
    retriever = ScamKnowledgeRetriever(
        knowledge_dir=settings.assistant_knowledge_dir,
        vector_dir=settings.assistant_vector_dir,
        embedding_model=settings.assistant_embedding_model,
    )
    chunks = retriever.build_index()
    print(f"Built ScamShieldAI assistant vector index with {chunks} chunks")


if __name__ == "__main__":
    main()