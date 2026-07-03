from __future__ import annotations

from app.application.assistant_dto import AssistantChatResponse, AssistantProviderDTO, AssistantSourceDTO
from app.application.services.risk_scoring_service import RiskScoringService
from app.assistant.rag import ScamKnowledgeRetriever
from app.core.config import Settings

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_openai import ChatOpenAI
except Exception:  # pragma: no cover - optional assistant dependencies
    ChatGoogleGenerativeAI = None
    ChatOpenAI = None


class CybersecurityAssistantService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._risk = RiskScoringService(settings)
        self._retriever = ScamKnowledgeRetriever(
            knowledge_dir=settings.assistant_knowledge_dir,
            vector_dir=settings.assistant_vector_dir,
            embedding_model=settings.assistant_embedding_model,
        )

    def answer(self, *, question: str, message: str, provider: str | None = None) -> AssistantChatResponse:
        selected_provider = (provider or self._settings.assistant_provider).casefold()
        risk = self._risk.score(message)
        contexts = self._retriever.retrieve(f"{question}\n{message}", k=4)
        safety_advice = self._safety_advice(risk.level)
        prompt = self._build_prompt(question, message, risk, contexts, safety_advice)
        llm_answer = self._call_llm(selected_provider, prompt)
        used_llm = llm_answer is not None
        answer = llm_answer or self._fallback_answer(risk, safety_advice, contexts)

        return AssistantChatResponse(
            answer=answer,
            scam_explanation=self._scam_explanation(risk),
            risk_analysis=risk,
            safety_advice=safety_advice,
            sources=[AssistantSourceDTO(source=item.source, score=item.score, excerpt=item.content[:360]) for item in contexts],
            provider=AssistantProviderDTO(provider=selected_provider, model=self._model_for(selected_provider), used_llm=used_llm),
        )

    def _call_llm(self, provider: str, prompt: str) -> str | None:
        if provider == "openai" and ChatOpenAI is not None and self._settings.openai_api_key:
            model = ChatOpenAI(model=self._settings.assistant_model, api_key=self._settings.openai_api_key, temperature=0.2)
            return str(model.invoke(prompt).content)
        if provider == "gemini" and ChatGoogleGenerativeAI is not None and self._settings.gemini_api_key:
            model = ChatGoogleGenerativeAI(model=self._settings.assistant_model, google_api_key=self._settings.gemini_api_key, temperature=0.2)
            return str(model.invoke(prompt).content)
        if provider == "llama" and ChatOpenAI is not None and self._settings.llama_base_url:
            model = ChatOpenAI(
                model=self._settings.assistant_model,
                api_key=self._settings.llama_api_key or "local-llama",
                base_url=self._settings.llama_base_url,
                temperature=0.2,
            )
            return str(model.invoke(prompt).content)
        return None

    def _build_prompt(self, question, message, risk, contexts, safety_advice: list[str]) -> str:
        context_block = "\n\n".join(f"Source: {item.source}\n{item.content}" for item in contexts)
        return f"""You are ScamShieldAI, a cautious cybersecurity assistant.
Answer the user's question using the risk analysis and retrieved knowledge.
Do not tell scammers how to evade detection. Do not render suspicious URLs as clickable links.

User question:
{question}

Message under review:
{message}

Risk analysis:
Score: {risk.risk_score}
Level: {risk.level}
Reasons: {', '.join(risk.reasons)}

Safety advice:
{chr(10).join('- ' + item for item in safety_advice)}

Retrieved knowledge:
{context_block}

Return a concise answer with sections: Scam explanation, Risk analysis, Safety advice.
"""

    def _fallback_answer(self, risk, safety_advice: list[str], contexts) -> str:
        lines = [
            "Scam explanation:",
            self._scam_explanation(risk),
            "",
            "Risk analysis:",
            f"Risk score is {risk.risk_score} and level is {risk.level}.",
        ]
        if risk.reasons:
            lines.extend(f"- {reason}" for reason in risk.reasons)
        lines.extend(["", "Safety advice:"])
        lines.extend(f"- {item}" for item in safety_advice)
        if contexts:
            lines.extend(["", "Relevant knowledge:"])
            lines.extend(f"- {item.source}" for item in contexts[:3])
        return "\n".join(lines)

    def _scam_explanation(self, risk) -> str:
        if risk.level == "Dangerous":
            return "This message is dangerous because multiple scam indicators were detected."
        if risk.level == "Suspicious":
            return "This message is suspicious and should be independently verified before taking action."
        return "This message appears low risk based on the available signals, but unusual financial requests should still be verified."

    def _safety_advice(self, level: str) -> list[str]:
        if level == "Dangerous":
            return [
                "Do not click links or reply to the sender.",
                "Do not share OTPs, passwords, CVV numbers, seed phrases, or identity documents.",
                "Verify through the official app, website, or known phone number.",
                "Report the message to the platform, bank, or cybercrime authority.",
            ]
        if level == "Suspicious":
            return [
                "Pause before acting and verify the sender independently.",
                "Avoid sending money or personal information.",
                "Check official channels for account or transaction issues.",
            ]
        return [
            "No strong scam signals were found.",
            "Continue to verify unexpected financial or identity requests.",
        ]

    def _model_for(self, provider: str) -> str:
        if provider == "local":
            return "deterministic-rag-fallback"
        return self._settings.assistant_model