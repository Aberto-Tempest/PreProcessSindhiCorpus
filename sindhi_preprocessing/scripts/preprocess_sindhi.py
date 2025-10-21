# -*- coding: utf-8 -*-
"""
Sindhi Text Preprocessing Script
--------------------------------
This script cleans and preprocesses Sindhi text for NLP tasks.

It:
✅ Removes punctuation and non-text symbols (while preserving Sindhi script)
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
# Keep Sindhi characters, Arabic script, digits, spaces, and common punctuation
# Unicode blocks: Arabic \u0600-\u06FF, Arabic Extended-A \u0750-\u077F, Extended-B \u08A0-\u08FF
allowed_pattern = r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF0-9\s۔؟]"

clean_text = "".join(ch if re.match(allowed_pattern, ch) else " " for ch in text)

# === Step 4: Normalize whitespace ===
clean_text = re.sub(r"\s+", " ", clean_text).strip()

# === Step 5: Split text into sentences ===
# Sindhi sentences often end with ۔ or ؟
sentences = re.split(r"[۔؟!]", clean_text)
sentences = [s.strip() for s in sentences if s.strip()]

# === Step 6: Load stopwords efficiently using a set ===
# (Set lookup is O(1) — much faster than list)
with open(STOPWORDS_FILE, "r", encoding="utf-8") as f:
    stopwords = set(line.strip() for line in f if line.strip())

def remove_stopwords(sentence):
    """Remove Sindhi stopwords from a single sentence."""
    words = sentence.split()  # Split by spaces (jointed script remains intact)
    filtered = [w for w in words if w not in stopwords]
    return " ".join(filtered)

# === Step 7: Apply stopword removal ===
processed_sentences = [remove_stopwords(s) for s in sentences]

# === Step 8: Write cleaned text to output file ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for line in processed_sentences:
        f.write(line + "\n")

print("✅ Preprocessing complete!")
print(f"Cleaned corpus saved at: {OUTPUT_FILE}")
