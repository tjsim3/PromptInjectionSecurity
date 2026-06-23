import json
import sys

from config import CONFIG
from model import SimpleNN
from rules import score_rules
from vectorizer import Vectorizer


def load_resources(model_path="nnpi_model.npz", vocab_path="vocab.json"):
    model = SimpleNN.load(model_path, lr=CONFIG["learning_rate"])
    vectorizer = Vectorizer()
    vectorizer.load(vocab_path)
    return model, vectorizer


def predict_proba(text: str, model: SimpleNN, vectorizer: Vectorizer) -> float:
    features = vectorizer.transform([text])
    return float(model.predict_proba(features)[0])


def score_text(text: str, model: SimpleNN, vectorizer: Vectorizer):
    nn_score = predict_proba(text, model, vectorizer)
    rule_score = score_rules(text)
    final_score = CONFIG["nn_weight"] * nn_score + CONFIG["rule_weight"] * rule_score
    return {
        "risk_score": round(final_score, 3),
        "nn_score": round(nn_score, 3),
        "rule_score": round(rule_score, 3),
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read().strip()
    model, vectorizer = load_resources()
    result = score_text(text, model, vectorizer)
    print(json.dumps(result))
