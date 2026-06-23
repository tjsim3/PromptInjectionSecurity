import json
from pathlib import Path

src = Path("data/kaggle_dataset.jsonl")
dst = Path("data/kaggle_adapted.jsonl")
labels_map = {
    "malicious": 1,
    "benign": 0,
    "attack": 1,
    "none": 0,
    "jailbreaking": 1,
    "role_playing": 1,
    "obfuscation": 1,
    "data_leakage": 1,
    "code_execution": 1,
}

with src.open("r", encoding="utf-8") as fin, dst.open("w", encoding="utf-8") as fout:
    for line in fin:
        line = line.strip()
        if not line:
            continue
        item = json.loads(line)
        text = item.get("text") or item.get("prompt") or item.get("query")
        if text is None:
            raise ValueError(f"No text field in line: {line}")
        raw_label = item.get("label")
        if isinstance(raw_label, str):
            label = labels_map.get(raw_label.strip().lower())
            if label is None:
                if raw_label.isdigit():
                    label = int(raw_label)
                else:
                    raise ValueError(f"Unknown label: {raw_label}")
        else:
            label = int(raw_label)
        fout.write(json.dumps({"text": text, "label": label}, ensure_ascii=False) + "\n")

print(f"Created {dst}")
