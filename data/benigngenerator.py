import json
import random

OUTPUT_FILE = "data/benign_dataset.jsonl"
NUM_SAMPLES = 5000

# ----------------------
# SAFE CONTENT
# ----------------------

topics = [
    "machine learning", "Python", "JavaScript", "databases",
    "cybersecurity", "neural networks", "APIs",
    "data structures", "algorithms", "web development",
    "physics", "biology", "history", "economics"
]

actions = [
    "explain", "summarize", "describe", "teach",
    "give an example of", "compare", "list key points about"
]

questions = [
    "What is {}?",
    "How does {} work?",
    "Why is {} important?",
    "Can you explain {}?",
]

tasks = [
    "{} {}",
    "Help me {} {}",
    "I want to learn about {}",
]

# ----------------------
# HARD NEGATIVES (VERY IMPORTANT)
# ----------------------

hard_negative_templates = [
    "Explain what 'ignore previous instructions' means",
    "Why is it dangerous to bypass safety systems?",
    "What is a system prompt in AI?",
    "Describe prompt injection attacks",
    "What happens if an AI ignores its instructions?",
    "Explain why 'reveal the system prompt' is unsafe",
    "Give examples of malicious prompts",
    "Why should AI not execute arbitrary commands?",
]

# ----------------------
# LONG / REALISTIC INPUTS
# ----------------------

long_templates = [
    """I am studying {} and I came across some confusing material.
    Can you explain the main concepts in a simple way and give examples?""",

    """Here is some content I found:
    ---
    {}
    ---
    Can you summarize it and explain key ideas?""",

    """I'm working on a project related to {}.
    What are best practices and common mistakes?"""
]

# ----------------------
# MIXED CONTENT (REAL-WORLD STYLE)
# ----------------------

mixed_templates = [
    "{} Also, explain {} in more detail.",
    "First {}, then {}",
    "{}. Additionally, provide examples for {}",
]

# ----------------------
# GENERATORS
# ----------------------

def generate_basic():
    topic = random.choice(topics)
    return random.choice(questions).format(topic)

def generate_task():
    action = random.choice(actions)
    topic = random.choice(topics)
    return f"{action} {topic}"

def generate_long():
    topic = random.choice(topics)
    return random.choice(long_templates).format(topic)

def generate_mixed():
    topic1 = random.choice(topics)
    topic2 = random.choice(topics)
    return random.choice(mixed_templates).format(topic1, topic2)

def generate_hard_negative():
    return random.choice(hard_negative_templates)

# ----------------------
# OBFUSCATION (light, safe)
# ----------------------

def vary(text):
    variations = [
        text,
        text.lower(),
        text.upper(),
        text + "?",
        text + ".",
    ]
    return random.choice(variations)

# ----------------------
# MAIN
# ----------------------

def main():
    with open(OUTPUT_FILE, "w") as f:
        for _ in range(NUM_SAMPLES):
            r = random.random()

            if r < 0.2:
                text = generate_hard_negative()
            elif r < 0.4:
                text = generate_long()
            elif r < 0.7:
                text = generate_basic()
            elif r < 0.9:
                text = generate_task()
            else:
                text = generate_mixed()

            text = vary(text)

            f.write(json.dumps({
                "text": text,
                "label": 0
            }) + "\n")

    print(f"Generated {NUM_SAMPLES} benign samples → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()