#!/usr/bin/env bash
# -------------------------------------------------------------
# 📜 Sindhi NLP Font Setup Script (with auto-check)
# Downloads and verifies Urdu/Sindhi-compatible fonts for
# Matplotlib and WordCloud visualization.
# -------------------------------------------------------------

set -e

FONT_DIR="fonts"
mkdir -p "$FONT_DIR"

# Helper to download a font if not present
download_if_missing() {
  local url="$1"
  local dest="$2"
  if [ ! -f "$dest" ]; then
    echo "📦 Downloading $(basename "$dest") ..."
    curl -L -o "$dest" "$url" || { echo "❌ Failed to download $dest"; exit 1; }
  else
    echo "✅ $(basename "$dest") already exists."
  fi
}

echo "🔍 Checking required fonts..."

# Noto Nastaliq Urdu
download_if_missing \
  "https://github.com/google/fonts/raw/main/ofl/notonastaliqurdu/NotoNastaliqUrdu-Regular.ttf" \
  "$FONT_DIR/NotoNastaliqUrdu-Regular.ttf"

# Noto Sans Arabic
download_if_missing \
  "https://github.com/google/fonts/raw/main/ofl/notosansarabic/NotoSansArabic-Regular.ttf" \
  "$FONT_DIR/NotoSansArabic-Regular.ttf"

echo "🔍 Verifying fonts..."
file "$FONT_DIR"/*.ttf || echo "⚠️ Font verification incomplete (file command missing)."

echo "✅ Fonts ready! You can now run:"
echo "python scripts/analyze_sindhi_corpus.py --data-dir data --out-dir processed/analysis_outputs --font-path ./fonts/NotoNastaliqUrdu-Regular.ttf"
