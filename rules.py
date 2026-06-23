import re

from config import CONFIG

PATTERNS = [
    r"(ignore|override|disregard).*(previous|instructions|rules)",
    r"(do not|don't) follow.*(previous|instructions|rules)",
    r"system prompt",
    r"now reply|now answer|answer only",
    r"forget the earlier conversation",
]


def score_rules(text: str) -> float:
    clean = text.lower()
    score = 0.0
    for pattern in PATTERNS:
        if re.search(pattern, clean):
            score += 0.25
    keyword_hits = sum(1 for kw in CONFIG["keyword_features"] if kw in clean)
    score += min(keyword_hits * 0.08, 0.3)
    score += min(len(re.findall(r"\b(ignore|override|system|prompt|now)\b", clean)) * 0.05, 0.4)
    return min(score, 1.0)
