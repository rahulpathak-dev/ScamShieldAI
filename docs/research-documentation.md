# Research Documentation

## Research Title

ScamShieldAI: An NLP and LLM-Powered Framework for Detection, Risk Scoring and Explainable AI-Based Analysis of Psychological Persuasion Strategies in Online Financial Scams

## Research Objective

Build a scalable cybersecurity platform that detects online financial scams, identifies persuasion strategies, assigns risk scores, and explains model decisions in human-readable form.

## Research Questions

1. How accurately can NLP and transformer models classify financial scam messages across digital channels?
2. Which psychological persuasion strategies are most predictive of scam risk?
3. Can explainable AI improve user trust and incident response quality?
4. How can multilingual and multimodal inputs be normalized into a shared risk scoring pipeline?

## Methodology

1. Data collection from SMS spam, phishing, financial fraud, scam report, and synthetic examples.
2. Preprocessing with cleaning, tokenization, normalization, and language detection.
3. Baseline modeling with TF-IDF, Logistic Regression, Random Forest, and SVM.
4. Advanced modeling with BERT and RoBERTa.
5. Persuasion strategy detection using keyword analysis and transformer classification.
6. Risk scoring from model prediction, persuasion signals, suspicious keywords, URLs, threat intelligence, and reports.
7. Explainability through SHAP, LIME, attention summaries, and human-readable explanations.
8. Evaluation with accuracy, precision, recall, F1, confusion matrices, and qualitative explanation review.

## Supported Scam Categories

- Phishing
- Banking fraud
- Investment scams
- Crypto scams
- Romance scams
- Job scams
- Lottery scams
- Identity theft
- Social engineering

## Persuasion Strategies

- Urgency
- Fear
- Authority manipulation
- Greed
- Scarcity
- Emotional pressure
- Fake trust
- Social engineering
- Impersonation

## Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1 score
- False positive rate
- False negative rate
- Explanation usefulness rating
- Latency per scan

## Ethics and Safety

- Minimize storage of sensitive user messages.
- Redact secrets, OTPs, credentials, and identity documents from logs.
- Avoid automated law-enforcement or financial decisions without human review.
- Provide transparent explanations and safety advice.
- Document dataset provenance and bias risks.