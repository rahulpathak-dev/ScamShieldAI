from app.ml.preprocessing import clean_text, tokenize


def test_clean_text_normalizes_security_entities():
    text = "URGENT! Pay ₹5,000 at https://bad.example/login or call +1 (555) 111-2222"

    cleaned = clean_text(text)

    assert "url_token" in cleaned
    assert "phone_token" in cleaned
    assert "money_token" in cleaned
    assert "urgent" in cleaned


def test_tokenize_returns_clean_tokens():
    tokens = tokenize("Verify your OTP now")

    assert tokens == ["verify", "your", "otp", "now"]