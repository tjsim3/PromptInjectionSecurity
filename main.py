import json
import sys

from config import CONFIG
from predict import load_input_text, load_resources, score_text


def risk_level(score: float) -> str:
    if score >= CONFIG["thresholds"]["high"]:
        return "HIGH"
    if score >= CONFIG["thresholds"]["medium"]:
        return "MEDIUM"
    return "LOW"


def main():
    if len(sys.argv) > 1:
        text = load_input_text(sys.argv[1] if len(sys.argv) == 2 else " ".join(sys.argv[1:]))
    else:
        text = load_input_text(sys.stdin.read().strip())
    model, vectorizer = load_resources()
    result = score_text(text, model, vectorizer)
    result["risk_level"] = risk_level(result["risk_score"])
    print(json.dumps(result))


if __name__ == "__main__":
    main()
