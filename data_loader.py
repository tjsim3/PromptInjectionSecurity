import json
from typing import List, Tuple


def load_jsonl(path: str) -> Tuple[List[str], List[int]]:
    texts = []
    labels = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            texts.append(item["text"])
            labels.append(int(item["label"]))
    return texts, labels
