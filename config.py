CONFIG = {
    "vocab_size": 2000,
    "use_ngrams": True,
    "ngram_range": (1, 2),
    "hidden_layers": [64, 32],
    "learning_rate": 0.01,
    "epochs": 250,
    "batch_size": 32,
    "nn_weight": 0.7,
    "rule_weight": 0.3,
    "thresholds": {
        "high": 0.7,
        "medium": 0.4,
    },
    "activation": "relu",
    "keyword_features": ["ignore", "system", "prompt", "override", "rules"],
}
