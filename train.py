import sys

import numpy as np

from config import CONFIG
from data_loader import load_jsonl
from model import SimpleNN
from vectorizer import Vectorizer
from data.riskgenerator import main as generate_data
from data.benigngenerator import main as generate_benign_data


np.random.seed(1)


def load_data(paths: list[str]):
    texts = []
    labels = []
    for path in paths:
        t, l = load_jsonl(path)
        texts.extend(t)
        labels.extend(l)
    return texts, labels


def train(paths: list[str]):
    texts, labels = load_data(paths)
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
    if os.path.exists("data/injection_dataset.jsonl"):
        os.remove("data/injection_dataset.jsonl")
    if os.path.exists("data/benign_dataset.jsonl"):
        os.remove("data/benign_dataset.jsonl")


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 1 and args[0] == "clear":
        clear()
        sys.exit(0)
    if len(args) == 1 and args[0] == "generate":
        generate_data()
        generate_benign_data()
        train(["data/injection_dataset.jsonl", "data/benign_dataset.jsonl"])
        sys.exit(0)
    if not args:
        args = ["data/sample_dataset.jsonl"]
    paths = [arg if arg.startswith("data/") else f"data/{arg}" for arg in args]
    print(f"training from: {', '.join(paths)}")
    try:
        train(paths)
    except Exception as e:
        print(f"Error: {e}")
        print("Usage: python train.py [path_to_jsonl_file ...]")
        sys.exit(1)
