import hashlib
import re
from collections import defaultdict

from app.domain.entities import (
    Evidence,
    PersuasionStrategy,
    RiskLevel,
    ScamAnalysis,
    ScamCategory,
    SourceType,
)


class ScamRiskEngine:
    """Explainable deterministic baseline for scam analysis."""

    _category_terms: dict[ScamCategory, tuple[str, ...]] = {
        ScamCategory.phishing: ("verify", "login", "password", "otp", "account locked", "click"),
        ScamCategory.banking_fraud: ("bank", "debit", "credit card", "transaction", "suspended"),
        ScamCategory.investment_scam: ("investment", "profit", "guaranteed return", "trading", "forex"),
        ScamCategory.crypto_scam: ("crypto", "bitcoin", "wallet", "seed phrase", "usdt"),
        ScamCategory.romance_scam: ("love", "relationship", "emergency money", "gift card"),
        ScamCategory.job_scam: ("job offer", "work from home", "registration fee", "hiring"),
        ScamCategory.lottery_scam: ("lottery", "winner", "prize", "claim reward"),
        ScamCategory.identity_theft: ("ssn", "aadhaar", "passport", "identity", "kyc"),
        ScamCategory.social_engineering: ("do not tell", "secret", "trust me", "urgent help"),
    }

    _strategy_terms: dict[PersuasionStrategy, tuple[str, ...]] = {
        PersuasionStrategy.urgency: ("urgent", "immediately", "now", "within 24 hours", "act fast"),
        PersuasionStrategy.authority_impersonation: ("bank", "irs", "police", "support team", "security department"),
        PersuasionStrategy.scarcity: ("limited time", "only today", "last chance", "few spots"),
        PersuasionStrategy.reward_promise: ("prize", "bonus", "guaranteed", "double your money", "reward"),
        PersuasionStrategy.fear_or_threat: ("suspended", "blocked", "legal action", "penalty", "arrest"),
        PersuasionStrategy.secrecy: ("confidential", "do not share", "do not tell", "secret"),
        PersuasionStrategy.trust_building: ("trusted", "verified", "official", "secure"),
        PersuasionStrategy.reciprocity: ("processing fee", "small fee", "refund after", "advance payment"),
    }

    _indicator_terms: tuple[tuple[str, str, float], ...] = (
        ("credential_request", "Requests sensitive credentials or OTP information.", 22.0),
        ("payment_pressure", "Pressures the recipient to pay a fee or transfer funds.", 18.0),
        ("external_link", "Contains a URL that may route the recipient outside a trusted channel.", 14.0),
        ("contact_shift", "Attempts to move the conversation to another channel.", 10.0),
    )

    def analyze(self, *, content: str, source_type: SourceType, language: str) -> ScamAnalysis:
        normalized = self._normalize(content)
        evidence: list[Evidence] = []

        category_scores = self._match_enum_terms(normalized, self._category_terms)
        strategy_scores = self._match_enum_terms(normalized, self._strategy_terms)

        for category, terms in category_scores.items():
            evidence.append(
                Evidence(
                    signal=f"category:{category.value}",
                    description=f"Message matches known {category.value.replace('_', ' ')} language.",
                    weight=min(18.0, 6.0 * len(terms)),
                    matched_terms=terms,
                )
            )

        for strategy, terms in strategy_scores.items():
            evidence.append(
                Evidence(
                    signal=f"strategy:{strategy.value}",
                    description=f"Persuasion strategy detected: {strategy.value.replace('_', ' ')}.",
                    weight=min(14.0, 5.0 * len(terms)),
                    matched_terms=terms,
                )
            )

        evidence.extend(self._indicator_evidence(normalized))

        risk_score = min(100.0, round(sum(item.weight for item in evidence), 2))
        risk_level = self._risk_level(risk_score)

        categories = sorted(category_scores, key=lambda item: item.value)
        strategies = sorted(strategy_scores, key=lambda item: item.value)

        if risk_score >= 60 and ScamCategory.social_engineering not in categories:
            categories.append(ScamCategory.social_engineering)

        return ScamAnalysis.create(
            source_type=source_type,
            language=language,
            content_sha256=hashlib.sha256(content.encode("utf-8")).hexdigest(),
            risk_score=risk_score,
            risk_level=risk_level,
            scam_categories=categories,
            persuasion_strategies=strategies,
            evidence=evidence,
            recommended_actions=self._recommended_actions(risk_level),
        )

    def _match_enum_terms(self, normalized: str, term_map):
        matches = defaultdict(list)
        for enum_value, terms in term_map.items():
            for term in terms:
                if term in normalized:
                    matches[enum_value].append(term)
        return dict(matches)

    def _indicator_evidence(self, normalized: str) -> list[Evidence]:
        evidence: list[Evidence] = []

        if re.search(r"\b(otp|password|pin|seed phrase|private key|cvv)\b", normalized):
            evidence.append(
                Evidence(
                    signal="credential_request",
                    description="Requests sensitive authentication or recovery data.",
                    weight=22.0,
                    matched_terms=["otp/password/pin/seed phrase/private key/cvv"],
                )
            )

        if re.search(r"\b(pay|transfer|deposit|fee|gift card|wire)\b", normalized):
            evidence.append(
                Evidence(
                    signal="payment_pressure",
                    description="Mentions payment, transfer, deposit, fee, or gift card language.",
                    weight=18.0,
                    matched_terms=["pay/transfer/deposit/fee/gift card/wire"],
                )
            )

        if re.search(r"https?://|www\.|bit\.ly|tinyurl", normalized):
            evidence.append(
                Evidence(
                    signal="external_link",
                    description="Contains an external link or shortened URL.",
                    weight=14.0,
                    matched_terms=["url"],
                )
            )

        if re.search(r"\b(whatsapp|telegram|signal|text me|call this number)\b", normalized):
            evidence.append(
                Evidence(
                    signal="contact_shift",
                    description="Attempts to shift the conversation to another channel.",
                    weight=10.0,
                    matched_terms=["alternate channel"],
                )
            )

        return evidence

    def _risk_level(self, score: float) -> RiskLevel:
        if score >= 85:
            return RiskLevel.critical
        if score >= 60:
            return RiskLevel.high
        if score >= 30:
            return RiskLevel.medium
        return RiskLevel.low

    def _recommended_actions(self, risk_level: RiskLevel) -> list[str]:
        if risk_level in {RiskLevel.high, RiskLevel.critical}:
            return [
                "Do not click links, share OTPs, send money, or continue the conversation.",
                "Verify the sender through an official website, phone number, or app.",
                "Report the message to the relevant platform, bank, or cybercrime authority.",
            ]
        if risk_level == RiskLevel.medium:
            return [
                "Verify the sender independently before taking action.",
                "Avoid sharing personal, banking, or identity information.",
            ]
        return ["No strong scam indicators were detected, but continue to verify unusual requests."]

    def _normalize(self, content: str) -> str:
        return re.sub(r"\s+", " ", content.casefold()).strip()

