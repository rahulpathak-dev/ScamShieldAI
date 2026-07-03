import re
from typing import Dict, List


class ScamAnalyzer:
    """Rule-based scam analyzer for the initial ScamShieldAI module."""

    def __init__(self) -> None:
        self.phishing_keywords = ["verify", "suspended", "urgent", "password", "bank", "account"]
        self.investment_keywords = ["guaranteed", "profit", "crypto", "investment", "join now"]
        self.persuasion_map = {
            "urgency": ["urgent", "immediately", "now"],
            "fear": ["suspended", "blocked", "penalty"],
            "greed": ["guaranteed", "profit", "double"],
        }

    def analyze(self, message: str) -> Dict[str, object]:
        normalized = message.lower()

        if any(keyword in normalized for keyword in self.phishing_keywords):
            category = "phishing"
            risk_score = 75
        elif any(keyword in normalized for keyword in self.investment_keywords):
            category = "investment"
            risk_score = 82
        else:
            category = "safe"
            risk_score = 10

        strategies = self._detect_strategies(normalized)

        return {
            "category": category,
            "risk_score": risk_score,
            "persuasion_strategies": strategies,
            "explanation": self._build_explanation(category, strategies),
        }

    def _detect_strategies(self, normalized: str) -> List[str]:
        strategies: List[str] = []
        for strategy, keywords in self.persuasion_map.items():
            if any(keyword in normalized for keyword in keywords):
                strategies.append(strategy)
        return strategies

    def _build_explanation(self, category: str, strategies: List[str]) -> str:
        if category == "safe":
            return "No suspicious scam indicators were found."

        strategy_text = ", ".join(strategies) if strategies else "manipulative language"
        return f"The message appears to be a {category} scam because it uses {strategy_text}."
