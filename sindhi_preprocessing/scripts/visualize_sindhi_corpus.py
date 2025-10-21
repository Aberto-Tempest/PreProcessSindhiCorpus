#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 visualize_sindhi_corpus.py
-----------------------------------------
Generates visualization plots for Sindhi text analysis.
Works with CSVs containing:
  • word           – disjointed token form
  • frequency      – count of the word
  • word_prepared  – joined form (for display)

Creates:
  • Bar Plot (Top frequent words)
  • Box Plot (Word length distribution)
  • Scatter Plot (Frequency vs Word length)
"""

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def visualize_sindhi_corpus(freq_file, out_dir, font_path=None):
    # --- Load Data ---
    if not os.path.exists(freq_file):
        raise FileNotFoundError(f"❌ Frequency file not found: {freq_file}")

    df = pd.read_csv(freq_file)
    expected_cols = {"word", "frequency", "word_prepared"}
    if not expected_cols.issubset(df.columns):
        raise ValueError(f"❌ CSV must contain columns: {expected_cols}")

    # --- Compute lengths ---
    df["length"] = df["word_prepared"].astype(str).apply(len)

    # --- Font Setup ---
    if font_path and os.path.exists(font_path):
        plt.rcParams["font.family"] = "sans-serif"
        plt.rcParams["font.sans-serif"] = [font_path]
        print(f"📝 Using font: {font_path}")
    else:
        print("⚠️ Custom font not found. Using default (may break Sindhi joins).")

    plt.rcParams["axes.unicode_minus"] = False
    os.makedirs(out_dir, exist_ok=True)

    # --- BAR PLOT (Top 20) ---
    plt.figure(figsize=(10, 6))
    top20 = df.nlargest(20, "frequency")
    plt.barh(top20["word_prepared"], top20["frequency"], color="teal")
    plt.gca().invert_yaxis()
    plt.title("🔥 Top 20 Most Frequent Sindhi Words (Joined Form)")
    plt.xlabel("Frequency")
    plt.tight_layout()
    bar_path = os.path.join(out_dir, "barplot_top20.png")
    plt.savefig(bar_path, dpi=300)
    plt.close()
    print(f"✅ Saved: {bar_path}")

    # --- BOX PLOT (Word Lengths) ---
    plt.figure(figsize=(6, 6))
    plt.boxplot(df["length"], patch_artist=True, boxprops=dict(facecolor="skyblue"))
    plt.title("📦 Word Length Distribution (Based on Joined Words)")
    plt.ylabel("Length of Words")
    plt.tight_layout()
    box_path = os.path.join(out_dir, "boxplot_word_length.png")
    plt.savefig(box_path, dpi=300)
    plt.close()
    print(f"✅ Saved: {box_path}")

    # --- SCATTER PLOT (Freq vs Length) ---
    plt.figure(figsize=(8, 6))
    plt.scatter(df["length"], df["frequency"], alpha=0.6, color="purple", edgecolors="w")
    plt.title("⚪ Frequency vs Word Length (Sindhi Corpus)")
    plt.xlabel("Word Length (Joined Form)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    scatter_path = os.path.join(out_dir, "scatter_freq_length.png")
    plt.savefig(scatter_path, dpi=300)
    plt.close()
    print(f"✅ Saved: {scatter_path}")

    print("\n🎉 Visualization complete! Check:", out_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize Sindhi corpus analysis results.")
    parser.add_argument("--freq-file", required=True, help="Path to word_frequency.csv")
    parser.add_argument("--out-dir", required=True, help="Output directory for plots")
    parser.add_argument("--font-path", help="Optional path to Sindhi/Arabic font (TTF)")
    args = parser.parse_args()

    visualize_sindhi_corpus(args.freq_file, args.out_dir, args.font_path)
