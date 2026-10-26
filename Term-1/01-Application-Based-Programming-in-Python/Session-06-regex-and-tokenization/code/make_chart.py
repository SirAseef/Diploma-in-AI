"""Tokenize a paragraph and plot the most frequent words -> ../images/top_tokens.png"""
import re
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

paragraph = """Artificial intelligence helps computers learn from data. Machine learning is a part of
artificial intelligence, and deep learning is a part of machine learning. With good data, a learning
model can find patterns, and those patterns help people make better decisions. Data is the fuel of AI;
models are the engine. Clean data, careful models and honest evaluation make AI useful."""
stop = {"a", "is", "the", "of", "and", "can", "are", "from", "with", "those", "make", "help", "helps"}
tokens = [t for t in re.findall(r"[a-z]+", paragraph.lower()) if t not in stop]
top = Counter(tokens).most_common(8)
words, counts = zip(*top)
fig, ax = plt.subplots(figsize=(6.5, 3.8))
ax.barh(words[::-1], counts[::-1], color="#1565c0")
ax.set_xlabel("frequency"); ax.set_title("Top tokens after regex tokenization + stop-word removal")
fig.tight_layout(); fig.savefig("../images/top_tokens.png", dpi=120)
print(top)
