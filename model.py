import numpy as np


class SimpleNN:
    def __init__(self, input_size, hidden_layers, activation="relu", lr=0.01):
        self.activation = activation
        self.lr = lr
        sizes = [input_size] + list(hidden_layers) + [1]
        self.weights = [
            np.random.randn(sizes[i], sizes[i + 1]).astype(np.float32) * np.sqrt(2 / max(1, sizes[i]))
            for i in range(len(sizes) - 1)
        ]
        self.biases = [np.zeros((sizes[i + 1],), dtype=np.float32) for i in range(len(sizes) - 1)]

    def _activate(self, x):
        if self.activation == "tanh":
            return np.tanh(x)
        return np.maximum(0.0, x)

    def _activate_grad(self, x):
        if self.activation == "tanh":
            return 1.0 - np.tanh(x) ** 2
        return (x > 0).astype(np.float32)

    def _sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def forward(self, X):
        activations = [X]
        preacts = []
        for W, b in zip(self.weights[:-1], self.biases[:-1]):
            Z = activations[-1] @ W + b
            preacts.append(Z)
            activations.append(self._activate(Z))
        Z = activations[-1] @ self.weights[-1] + self.biases[-1]
        preacts.append(Z)
        return self._sigmoid(Z), activations, preacts

    def predict_proba(self, X):
        probs, _, _ = self.forward(X)
        return probs.ravel()

    def loss(self, y_pred, y_true):
        y_pred = np.clip(y_pred, 1e-7, 1.0 - 1e-7)
        return -np.mean(y_true * np.log(y_pred) + (1.0 - y_true) * np.log(1.0 - y_pred))

    def train_step(self, X, y):
        y = y.reshape(-1, 1)
        y_pred, activations, preacts = self.forward(X)
        loss = self.loss(y_pred, y)
        grad = (y_pred - y) / X.shape[0]
        dWs = []
        dbs = []
        for i in reversed(range(len(self.weights))):
            a_prev = activations[i]
            dW = a_prev.T @ grad
            db = np.sum(grad, axis=0)
            dWs.insert(0, dW)
            dbs.insert(0, db)
            if i > 0:
                grad = (grad @ self.weights[i].T) * self._activate_grad(preacts[i - 1])
        for i in range(len(self.weights)):
            self.weights[i] -= self.lr * dWs[i]
            self.biases[i] -= self.lr * dbs[i]
        return loss

    def save(self, path: str):
        payload = {"activation": self.activation}
        for i, W in enumerate(self.weights):
            payload[f"W{i}"] = W
        for i, b in enumerate(self.biases):
            payload[f"b{i}"] = b
        np.savez_compressed(path, **payload)

    @classmethod
    def load(cls, path: str, lr=0.01):
        payload = np.load(path, allow_pickle=True)
        weight_keys = [k for k in payload.files if k.startswith("W")]
        bias_keys = [k for k in payload.files if k.startswith("b")]
        weights = [payload[f"W{i}"] for i in range(len(weight_keys))]
        biases = [payload[f"b{i}"] for i in range(len(bias_keys))]
        nn = cls.__new__(cls)
        nn.weights = weights
        nn.biases = biases
        activation = payload["activation"]
        nn.activation = activation.tolist() if hasattr(activation, "tolist") else str(activation)
        nn.lr = lr
        return nn
