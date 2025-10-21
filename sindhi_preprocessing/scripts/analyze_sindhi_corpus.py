# -*- coding: utf-8 -*-
"""
Sindhi Corpus Analysis Script
-----------------------------
Performs analysis and visualization on both raw and cleaned Sindhi text corpora.

Features:
✅ Token and sentence statistics
✅ Word frequency distribution
✅ Word cloud visualization
✅ Pre vs Post preprocessing comparison

Run:
    python3 scripts/analyze_sindhi_corpus.py
"""

import os
import re
import unicodedata
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# === Step 1: File paths ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

RAW_FILE = os.path.join(DATA_DIR, "raw_corpus.txt")
CLEANED_FILE = os.path.join(DATA_DIR, "cleaned_corpus.txt")

# === Step 2: Load text files safely (UTF-8 + NFC normalization) ===
def load_text(path):
    """Load UTF-8 text and normalize to NFC form to preserve Sindhi script joining."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return unicodedata.normalize("NFC", text)

raw_text = load_text(RAW_FILE)
cleaned_text = load_text(CLEANED_FILE)

# === Step 3: Tokenization and sentence splitting ===
# Sindhi uses "۔" (full stop) and "؟" (question mark) for sentence boundaries
def split_sentences(text):
    return [s.strip() for s in re.split(r"[۔؟!]", text) if s.strip()]

def tokenize(text):
    """Tokenize Sindhi text without breaking script joins (split by whitespace)."""
    return [w for w in text.split() if w.strip()]

raw_sentences = split_sentences(raw_text)
cleaned_sentences = split_sentences(cleaned_text)

raw_tokens = tokenize(raw_text)
cleaned_tokens = tokenize(cleaned_text)

# === Step 4: Compute statistics ===
def corpus_stats(name, sentences, tokens):
    print(f"\n📊 {name} Corpus Statistics:")
    print(f"  • Sentences: {len(sentences)}")
    print(f"  • Tokens: {len(tokens)}")
    avg_len = len(tokens) / max(len(sentences), 1)
    print(f"  • Avg. Tokens per Sentence: {avg_len:.2f}")

corpus_stats("Raw", raw_sentences, raw_tokens)
corpus_stats("Cleaned", cleaned_sentences, cleaned_tokens)

# === Step 5: Frequency Distribution ===
def get_freq(tokens):
    return Counter(tokens)

raw_freq = get_freq(raw_tokens)
cleaned_freq = get_freq(cleaned_tokens)

# === Step 6: Visualization: Word Frequency Bar Chart ===
def plot_top_words(freq, title, top_n=20):
    """Plot top N most frequent Sindhi words using Matplotlib."""
    common = freq.most_common(top_n)
    words, counts = zip(*common)
    plt.figure(figsize=(10, 6))
    plt.barh(words, counts)
    plt.gca().invert_yaxis()
    plt.title(title, fontsize=14)
    plt.xlabel("Frequency")
    plt.ylabel("Word")
    plt.tight_layout()
    plt.show()

plot_top_words(cleaned_freq, "Top 20 Most Frequent Words (Cleaned Corpus)")

# === Step 7: Word Cloud Visualization ===
def generate_wordcloud(freq):
    """Generate a Sindhi word cloud visualization."""
    wc = WordCloud(
        font_path="/usr/share/fonts/truetype/noto/NotoNastaliqUrdu-Regular.ttf",  # RTL-safe font
        width=800,
        height=400,
        background_color="white",
        colormap="plasma"
    ).generate_from_frequencies(freq)
    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Sindhi Word Cloud", fontsize=16)
    plt.show()

generate_wordcloud(cleaned_freq)

# === Step 8: Distribution Plot ===
def plot_word_distribution(freq, title="Word Frequency Distribution"):
    """Plot a simple frequency distribution curve."""
    counts = list(freq.values())
    counts.sort(reverse=True)
    plt.figure(figsize=(8, 5))
    plt.plot(counts)
    plt.title(title)
    plt.xlabel("Word Rank")
    plt.ylabel("Frequency")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

plot_word_distribution(cleaned_freq)

print("\n✅ Analysis complete! Visualizations displayed successfully.")
