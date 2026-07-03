# Module 008: AI Cybersecurity Assistant

## Goal

Build an AI assistant that answers user questions such as:

```text
Is this message dangerous?
```

The assistant provides:

- scam explanation
- risk analysis
- safety advice
- retrieved context from ScamShieldAI knowledge sources

## Providers

The assistant supports provider selection through one abstraction:

- OpenAI
- Gemini
- Llama through an OpenAI-compatible local/server endpoint
- Local deterministic fallback

Config:

```text
SCAMSHIELD_ASSISTANT_PROVIDER=local
SCAMSHIELD_ASSISTANT_MODEL=gpt-4.1-mini
SCAMSHIELD_OPENAI_API_KEY=
SCAMSHIELD_GEMINI_API_KEY=
SCAMSHIELD_LLAMA_BASE_URL=
SCAMSHIELD_LLAMA_API_KEY=
```

The `local` provider does not call an external LLM. It uses risk scoring and retrieved knowledge to generate a deterministic response.

## RAG System

Knowledge sources live in:

```text
knowledge/
```

Current sources:

- scam reports
- cybersecurity guidelines
- fraud examples

Files:

```text
knowledge/scam_reports.md
knowledge/cybersecurity_guidelines.md
knowledge/fraud_examples.md
```

Vector store path:

```text
ml/vectorstores/scamshield
```

Build the vector index:

```powershell
cd apps/api
pip install -r requirements-assistant.txt
python -m app.assistant.build_vector_index
```

If LangChain/FAISS dependencies or a vector index are unavailable, the assistant uses lexical retrieval over the markdown knowledge files.

## API

### `POST /api/v1/assistant/chat`

Request:

```json
{
  "question": "Is this message dangerous?",
  "message": "Urgent bank alert. Verify OTP now or your account will be suspended.",
  "provider": "local"
}
```

Response:

```json
{
  "answer": "Scam explanation:\nThis message is dangerous...",
  "scam_explanation": "This message is dangerous because multiple scam indicators were detected.",
  "risk_analysis": {
    "Risk Score": 78,
    "Level": "Dangerous",
    "Reasons": []
  },
  "safety_advice": [
    "Do not click links or reply to the sender.",
    "Do not share OTPs, passwords, CVV numbers, seed phrases, or identity documents."
  ],
  "sources": [],
  "provider": {
    "provider": "local",
    "model": "deterministic-rag-fallback",
    "used_llm": false
  }
}
```

## Architecture

```text
FastAPI route
  -> CybersecurityAssistantService
  -> RiskScoringService
  -> ScamKnowledgeRetriever
  -> provider adapter: OpenAI / Gemini / Llama / local
```

Files:

```text
apps/api/app/application/assistant_dto.py
apps/api/app/application/services/cybersecurity_assistant_service.py
apps/api/app/assistant/rag.py
apps/api/app/assistant/build_vector_index.py
apps/api/app/interfaces/api/v1/assistant.py
```

## LangChain and Vector Database

Assistant dependencies are isolated in:

```text
apps/api/requirements-assistant.txt
```

The vector database implementation is FAISS through LangChain. This keeps local development simple while preserving a clean boundary for replacing FAISS with a managed vector database later.

## Safety Rules

- The assistant should not explain how to bypass scam detection.
- Suspicious URLs must not be rendered as clickable links.
- Safety advice should prioritize independent verification and non-disclosure of sensitive credentials.
- The assistant should use retrieved context as grounding, but the risk scoring system remains the authoritative local signal.