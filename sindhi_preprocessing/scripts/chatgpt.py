# Arabic shaping / bidi for correct Arabic-script rendering
import arabic_reshaper
from bidi.algorithm import get_display
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from __future__ import annotations
import argparse
import csv
import os
import sys
import unicodedata
import re
from collections import Counter
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict

import matplotlib.pyplot as plt
from wordcloud import WordCloud

# -----------------------------
# Regex and utility definitions
# -----------------------------
# Match runs of characters from Arabic / Sindhi Unicode ranges listed in the prompt
ARABIC_SINDHI_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+")

# Sentence splitter (used only for optional raw analysis if sentences are present)
SENTENCE_SPLIT_RE = re.compile(r"[۔؟!?]+")

@dataclass
class CorpusStats:
    line_count: int
    word_count: int
    unique_word_count: int
    avg_word_length: float

# -----------------------------
# Core functions
# -----------------------------

def read_text_file(path: str) -> str:
    """Read a UTF-8 text file and return normalized (NFC) text."""
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    return unicodedata.normalize("NFC", raw)


def extract_words(text: str) -> List[str]:
    """Extract words that belong to Sindhi/Arabic Unicode ranges.

    This avoids splitting joined glyphs and is robust across whitespace
    and punctuation variations.
    """
    # Find all matches of Arabic/Sindhi runs and return them (lowercasing is not applied because
    # Arabic-script languages don't have case distinctions like Latin scripts).
    return ARABIC_SINDHI_RE.findall(text)


def compute_stats_from_text(text: str) -> Tuple[CorpusStats, Counter]:
    """Compute corpus statistics and word frequency counter from raw text."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    line_count = len(lines)

    words = extract_words(text)
    word_count = len(words)
    freq = Counter(words)

    unique_word_count = len(freq)
    avg_word_length = (sum(len(w) for w in words) / word_count) if word_count else 0.0

    stats = CorpusStats(
        line_count=line_count,
        word_count=word_count,
        unique_word_count=unique_word_count,
        avg_word_length=round(avg_word_length, 3),
    )
    return stats, freq


def save_word_frequency_csv(freq: Counter, out_path: str, top_n: int | None = None) -> None:
    """Save word frequency counts to CSV with columns: word, count, rank."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    items = freq.most_common(top_n)
    with open(out_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["rank", "word", "count"])
        for i, (w, c) in enumerate(items, start=1):
            writer.writerow([i, w, c])


def save_stats_csv(stats: CorpusStats, out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["metric", "value"])
        for k, v in asdict(stats).items():
            writer.writerow([k, v])

def shape_for_display(word: str) -> str:
    """
    Shape + reorder Arabic-script word for display in matplotlib/WordCloud.
    Returns a visual representation ready for plotting.
    """
    # arabic_reshaper.reshape returns shaped glyph sequence (ligatures)
    try:
        reshaped = arabic_reshaper.reshape(word)
        bidi = get_display(reshaped)
        return bidi
    except Exception:
        # if shaping fails for any reason, return original safely
        return word

def plot_top_frequency(freq: Counter, out_path: str, top_n: int = 30, font_path: str | None = None) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    most = freq.most_common(top_n)
    if not most:
        print("[warn] no tokens to plot for frequency distribution.")
        return

    words, counts = zip(*most)

    # If the user provided font_path, create a FontProperties for axis labels
    fp = FontProperties(fname=font_path) if font_path else None

    # reshape words for display
    disp_words = [shape_for_display(w) for w in words]

    plt.figure(figsize=(12, 6))
    plt.bar(range(len(disp_words)), counts)
    plt.xticks(range(len(disp_words)), disp_words, rotation=45, ha="right", fontproperties=fp)
    plt.xlabel("Words", fontproperties=fp)
    plt.ylabel("Frequency", fontproperties=fp)
    plt.title(f"Top {len(disp_words)} word frequency distribution", fontproperties=fp)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()


def generate_wordcloud(freq: Counter, out_path: str, font_path: str | None = None, max_words: int = 200) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if not freq:
        print("[warn] empty frequency; skipping wordcloud generation.")
        return

    # Create a shaped frequency dictionary for rendering
    shaped_freq = { shape_for_display(k): v for k, v in freq.items() }

    wc = WordCloud(
        width=1600,
        height=900,
        max_words=max_words,
        background_color="white",
        font_path=font_path,  # must point to an Arabic-supporting TTF
        collocations=False,
    )
    wc.generate_from_frequencies(shaped_freq)
    wc.to_file(out_path)

# -----------------------------
# Main CLI
# -----------------------------

def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze Sindhi corpus: stats, freq CSV, plots, wordcloud")
    parser.add_argument("--data-dir", default="data", help="Directory containing raw_corpus.txt and cleaned_corpus.txt")
    parser.add_argument("--out-dir", default="processed/analysis_outputs", help="Output directory for analysis artifacts")
    parser.add_argument("--font-path", default=None, help="Optional path to a TTF font that supports Arabic/Sindhi (recommended)")
    parser.add_argument("--top-n-words", type=int, default=200, help="How many words to include in wordcloud and CSV (default: 200)")
    parser.add_argument("--plot-top-n", type=int, default=30, help="Top N words to plot in the bar chart (default: 30)")
    args = parser.parse_args(argv)

    data_dir = args.data_dir
    out_dir = args.out_dir
    font_path = args.font_path

    raw_path = os.path.join(data_dir, "raw_corpus.txt")
    cleaned_path = os.path.join(data_dir, "cleaned_corpus.txt")

    if not os.path.exists(raw_path):
        print(f"[error] missing raw file: {raw_path}")
        return 2
    if not os.path.exists(cleaned_path):
        print(f"[error] missing cleaned file: {cleaned_path}")
        return 2

    print("Reading and analyzing raw corpus...")
    raw_text = read_text_file(raw_path)
    raw_stats, raw_freq = compute_stats_from_text(raw_text)

    print("Reading and analyzing cleaned corpus...")
    cleaned_text = read_text_file(cleaned_path)
    cleaned_stats, cleaned_freq = compute_stats_from_text(cleaned_text)

    # Save stats
    save_stats_csv(raw_stats, os.path.join(out_dir, "corpus_statistics_before.csv"))
    save_stats_csv(cleaned_stats, os.path.join(out_dir, "corpus_statistics_after.csv"))

    # Save frequency CSVs (top N)
    save_word_frequency_csv(cleaned_freq, os.path.join(out_dir, "word_frequency.csv"), top_n=args.top_n_words)

    # Create plots and wordcloud
    print("Generating frequency distribution plot and wordcloud (may warn if font missing)...")
    try:
        plot_top_frequency(cleaned_freq, os.path.join(out_dir, "frequency_distribution.png"), top_n=args.plot_top_n, font_path=font_path)

    except Exception as e:
        print(f"[error] failed to create frequency distribution plot: {e}")

    try:
        generate_wordcloud(cleaned_freq, os.path.join(out_dir, "wordcloud.png"), font_path=font_path, max_words=args.top_n_words)
    except Exception as e:
        print(f"[error] failed to create wordcloud: {e}")

    print(f"Analysis complete. Outputs in: {out_dir}")
    print("Important: for visually correct Sindhi/Arabic rendering, supply --font-path to a Nastaliq or Arabic font (eg. NotoSansArabic or NotoNastaliqUrdu).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
