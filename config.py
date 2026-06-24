CONFIG = {
    "vocab_size": 2000,
    "use_ngrams": True,
    "ngram_range": (1, 2),
    "hidden_layers": [64, 32],
    "learning_rate": 0.01,
    "epochs": 250,
    "batch_size": 32,
    "nn_weight": 0.75,
    "rule_weight": 0.25,
    "thresholds": {
        "high": 0.7,
        "medium": 0.4,
    },
    "activation": "relu",
    "keyword_features": ["ignore", "system", "prompt", "override", "rules"],
    "generate_data": {
        "num_samples": 5000,
        "output_file": "data/injection_dataset.jsonl",
        "output_benign_file": "data/benign_dataset.jsonl",
    },
}
