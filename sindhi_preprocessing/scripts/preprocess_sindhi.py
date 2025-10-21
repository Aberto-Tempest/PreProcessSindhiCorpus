# -*- coding: utf-8 -*-
"""
Sindhi Text Preprocessing Script
--------------------------------
This script cleans and preprocesses Sindhi text for NLP tasks.

It:
✅ Removes punctuation, numbers, and non-text symbols (while preserving Sindhi script)
✅ Normalizes Unicode (NFC form) to keep the script jointed
✅ Removes extra whitespace
✅ Splits text into readable lines or sentences
✅ Removes Sindhi stopwords using a provided file
✅ Saves the cleaned text into /processed/cleaned_corpus.txt

Run inside GitHub Codespaces terminal:
    python3 scripts/preprocess_sindhi.py
"""

import os
import re
import unicodedata

# === Step 1: Define file paths ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "processed")

INPUT_FILE = os.path.join(DATA_DIR, "raw_corpus.txt")
STOPWORDS_FILE = os.path.join(DATA_DIR, "sindhi_stopwords.txt")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "cleaned_corpus.txt")

# Make sure /processed directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Step 2: Read the raw Sindhi text file ===
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Normalize to NFC form to ensure jointed Sindhi script (important for cursive characters)
text = unicodedata.normalize("NFC", text)

# === Step 3: Remove unwanted characters ===
# ⛔️ Updated: Removed all digits (Western 0–9 and Arabic-Indic ٠–٩)
# Keep only Sindhi (Arabic-based) script, spaces, and Sindhi punctuation marks
# Unicode blocks: Arabic \u0600-\u06FF, Arabic Extended-A \u0750-\u077F, Extended-B \u08A0-\u08FF
# Removed digits 0–9 (\u0030-\u0039) and Arabic-Indic digits (\u0660-\u0669)
allowed_pattern = r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\s۔؟]"

# Replace disallowed characters with a space
clean_text = "".join(ch if re.match(allowed_pattern, ch) else " " for ch in text)

# === Step 4: Normalize whitespace ===
clean_text = re.sub(r"\s+", " ", clean_text).strip()

# === Step 5: Split text into sentences ===
# First split by Sindhi punctuation marks
sentences = re.split(r"[۔؟!]", clean_text)
sentences = [s.strip() for s in sentences if s.strip()]

# === Step 6: Further split long sentences by spaces ===
def split_long_sentences(sentences, max_words=15):
    """Split sentences that are too long into smaller chunks"""
    split_sentences = []
    for sentence in sentences:
        words = sentence.split()
        if len(words) <= max_words:
            split_sentences.append(sentence)
        else:
            # Split into chunks of max_words
            for i in range(0, len(words), max_words):
                chunk = " ".join(words[i:i + max_words])
                split_sentences.append(chunk)
    return split_sentences

# Apply sentence splitting
processed_sentences = split_long_sentences(sentences, max_words=10)  # Adjust max_words as needed

# === Step 7: Load stopwords efficiently using a set ===
# (Set lookup is O(1) — much faster than list)
with open(STOPWORDS_FILE, "r", encoding="utf-8") as f:
    stopwords = set(line.strip() for line in f if line.strip())

def remove_stopwords(sentence):
    """Remove Sindhi stopwords from a single sentence."""
    words = sentence.split()  # Split by spaces (jointed script remains intact)
    filtered = [w for w in words if w not in stopwords]
    return " ".join(filtered)

# === Step 8: Apply stopword removal ===
processed_sentences = [remove_stopwords(s) for s in processed_sentences]

# Remove any empty sentences after stopword removal
processed_sentences = [s for s in processed_sentences if s.strip()]

# === Step 9: Write cleaned text to output file ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for line in processed_sentences:
        f.write(line + "\n")

print("✅ Preprocessing complete!")
print(f"Original sentences: {len(sentences)}")
print(f"After splitting: {len(processed_sentences)}")
print(f"Cleaned corpus saved at: {OUTPUT_FILE}")