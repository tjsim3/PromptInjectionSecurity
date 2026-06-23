import sys

import numpy as np

from config import CONFIG
from data import load_jsonl
from model import SimpleNN
from vectorizer import Vectorizer

np.random.seed(1)


def train(path: str):
    texts, labels = load_jsonl(path)
    vectorizer = Vectorizer()
    X = vectorizer.fit_transform(texts)
    y = np.array(labels, dtype=np.float32)
    model = SimpleNN(
        X.shape[1],
        CONFIG["hidden_layers"],
        activation=CONFIG["activation"],
        lr=CONFIG["learning_rate"],
    )
    for epoch in range(1, CONFIG["epochs"] + 1):
        order = np.random.permutation(len(X))
        losses = []
        for start in range(0, len(X), CONFIG["batch_size"]):
            end = start + CONFIG["batch_size"]
            batch_X = X[order[start:end]]
            batch_y = y[order[start:end]]
            losses.append(model.train_step(batch_X, batch_y))
        if True:
            print(f"epoch {epoch}/{CONFIG['epochs']} loss={np.mean(losses):.4f}")
    model.save("nnpi_model.npz")
    vectorizer.save("vocab.json")
    pred = model.predict_proba(X)
    accuracy = np.mean((pred > 0.5) == y)
    print(f"saved nnpi_model.npz and vocab.json")
    print(f"train accuracy: {accuracy:.3f}")

def clear():
    import os

    if os.path.exists("nnpi_model.npz"):
        os.remove("nnpi_model.npz")
    if os.path.exists("vocab.json"):
        os.remove("vocab.json")


if __name__ == "__main__":
    if sys.argv[1] == "clear":
        clear()
    else:
        path = sys.argv[1] if len(sys.argv) > 1 else "data/sample_dataset.jsonl"
        train(path)
