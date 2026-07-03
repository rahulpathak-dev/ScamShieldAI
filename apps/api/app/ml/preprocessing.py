import html
import re
import unicodedata

URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
EMAIL_PATTERN = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
PHONE_PATTERN = re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{6,}\d)(?!\w)")
MONEY_PATTERN = re.compile(r"(?:[$\u20ac\u00a3\u20b9]\s?\d+(?:[,.]\d+)*)|(?:\d+(?:[,.]\d+)*\s?(?:usd|eur|gbp|inr|rs))", re.IGNORECASE)
WHITESPACE_PATTERN = re.compile(r"\s+")
NON_TEXT_PATTERN = re.compile(r"[^a-z0-9_@\s.!?%$\u20ac\u00a3\u20b9:/+-]")


def clean_text(text: str) -> str:
    value = html.unescape(str(text))
    value = unicodedata.normalize("NFKC", value)
    value = value.casefold()
    value = URL_PATTERN.sub(" url_token ", value)
    value = EMAIL_PATTERN.sub(" email_token ", value)
    value = PHONE_PATTERN.sub(" phone_token ", value)
    value = MONEY_PATTERN.sub(" money_token ", value)
    value = NON_TEXT_PATTERN.sub(" ", value)
    value = WHITESPACE_PATTERN.sub(" ", value)
    return value.strip()


def tokenize(text: str) -> list[str]:
    return clean_text(text).split()