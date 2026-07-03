import unittest
from app.services.analyzer import ScamAnalyzer


class ScamAnalyzerTests(unittest.TestCase):
    def test_detects_phishing_with_urgency_keywords(self):
        analyzer = ScamAnalyzer()
        result = analyzer.analyze("Urgent! Verify your bank account now or it will be suspended.")

        self.assertEqual(result["category"], "phishing")
        self.assertGreaterEqual(result["risk_score"], 70)
        self.assertIn("urgency", result["persuasion_strategies"])

    def test_detects_investment_scam_with_crypto_terms(self):
        analyzer = ScamAnalyzer()
        result = analyzer.analyze("Guaranteed 300% profit in crypto within 24 hours, join now!")

        self.assertEqual(result["category"], "investment")
        self.assertGreaterEqual(result["risk_score"], 80)


if __name__ == "__main__":
    unittest.main()
