import collections
import json
import re
from typing import List

import numpy as np

from config import CONFIG

TOKEN_RE = re.compile(r"\b\w+\b")


class Vectorizer:
    def __init__(self, config=CONFIG):
        self.config = config
        self.vocab = {}
        self.feature_names: List[str] = []

    def _tokenize(self, text: str) -> List[str]:
        return TOKEN_RE.findall(text.lower())

    def _ngrams(self, tokens: List[str]) -> List[str]:
        if not self.config["use_ngrams"]:
            return tokens
        features = []
        min_n, max_n = self.config["ngram_range"]
        for n in range(min_n, max_n + 1):
            if n == 1:
                features.extend(tokens)
            else:
                features.extend([" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)])
        return features

    def _extra_features(self, text: str) -> List[float]:
        clean = text.lower()
        flags = [1.0 if kw in clean else 0.0 for kw in self.config.get("keyword_features", [])]
        length = min(len(text) / 200.0, 1.0)
        return flags + [length]

    def fit(self, texts: List[str]):
        counter = collections.Counter()
        for text in texts:
            tokens = self._tokenize(text)
            counter.update(self._ngrams(tokens))
        for idx, token in enumerate(counter.most_common(self.config["vocab_size"])):
            self.vocab[token[0]] = idx
        self.feature_names = list(self.vocab) + self.config.get("keyword_features", []) + ["length"]
        return self

    def transform(self, texts: List[str]) -> np.ndarray:
        features = np.zeros((len(texts), len(self.feature_names)), dtype=np.float32)
        for row, text in enumerate(texts):
            for token in self._ngrams(self._tokenize(text)):
                if token in self.vocab:
                    features[row, self.vocab[token]] += 1.0
            features[row, len(self.vocab) :] = self._extra_features(text)
        return features

    def fit_transform(self, texts: List[str]) -> np.ndarray:
        self.fit(texts)
        return self.transform(texts)

    def save(self, path: str):
        payload = {"vocab": self.vocab, "feature_names": self.feature_names}
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)

    def load(self, path: str):
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        self.vocab = payload["vocab"]
        self.feature_names = payload["feature_names"]
        return self
