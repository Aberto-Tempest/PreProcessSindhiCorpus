## 🧠 `PROMPT_CONTEXT.md`

```markdown
# 🧠 Sindhi NLP Preprocessing Project – Context Prompt

## 📋 Overview

You are an **NLP engineer, data scientist, and software engineer** working inside **GitHub Codespaces**.

This project focuses on **preprocessing Sindhi text data** for natural language processing (NLP) and linguistic research.

The setup ensures **Unicode-safe**, **right-to-left–friendly**, and **cursive-preserving** preprocessing suitable for Sindhi, which uses the Arabic script.

---

## 🗂️ Project Structure

```

sindhi_preprocessing/
├── data/
│   ├── raw_corpus.txt            # Original Sindhi corpus (UTF-8 encoded)
│   └── sindhi_stopwords.txt      # Stopword list (UTF-8, one word per line)
├── processed/
│   └── cleaned_corpus.txt        # Cleaned, normalized, stopword-free text (output)
├── scripts/
│   └── preprocess_sindhi.py      # Main preprocessing script
├── README.md                     # Usage and setup instructions
└── PROMPT_CONTEXT.md             # This file (used for extending the project)

```

---

## ⚙️ Current Functionality Summary

The **`preprocess_sindhi.py`** script currently performs:

1. **Unicode Normalization**  
   Uses `unicodedata.normalize("NFC", text)` to ensure jointed Sindhi cursive script is preserved.

2. **Character Cleaning**  
   Removes punctuation and non-text symbols, keeping Sindhi/Arabic blocks:  
   `\u0600–\u06FF`, `\u0750–\u077F`, `\u08A0–\u08FF`, plus spaces, digits, and `۔`, `؟`.

3. **Whitespace Normalization**  
   Replaces multiple spaces/newlines with a single space.

4. **Sentence Segmentation**  
   Splits text into sentences using Sindhi punctuation (`۔`, `؟`, `!`).

5. **Stopword Removal**  
   Loads `sindhi_stopwords.txt` into a Python `set` for **O(1) lookup**  
   and removes common function words safely without breaking the jointed script.

6. **Output Generation**  
   Saves cleaned, stopword-free text into `/processed/cleaned_corpus.txt`,  
   one sentence per line — ready for NLP analysis.

---

## 🔒 Unicode & Script Safety Practices

- All text I/O uses `encoding="utf-8"`.
- NFC normalization keeps glyphs jointed in Sindhi’s cursive writing.
- Avoids splitting based on character code points to preserve letter joins.
- Works cleanly with RTL fonts such as *Noto Nastaliq Urdu* or *Noto Sans Arabic*.

---

## 🧾 Ready for Use In

- Tokenization  
- Word frequency analysis  
- Embedding generation (Word2Vec, FastText, etc.)  
- Corpus statistics  
- Model fine-tuning or translation pipelines  

---

## 🧭 EXTENSION GOAL (Add Here)

When you want to extend this project, **add your new feature request or goal below** this section.  
ChatGPT (or any LLM) will then understand the full context and generate the new module or improvement in a consistent, integrated way.

### Example:

```

🧭 EXTENSION GOAL:
Add a token frequency analyzer that counts the top 100 most common words after stopword removal
and saves the results as both CSV and bar chart (PNG) inside /processed/.

```

### Another Example:

```

🧭 EXTENSION GOAL:
Integrate a word embedding generator using gensim to create Sindhi Word2Vec vectors
from the cleaned_corpus.txt and store them as /processed/sindhi_embeddings.model.

````

---

## 🧩 Recommended Workflow

1. Copy this entire file’s content when you start a new ChatGPT session.  
2. Paste it as context so the model understands your project structure and goals.  
3. Add your **🧭 EXTENSION GOAL** at the end before submitting your request.  
4. Receive a context-aware response that integrates seamlessly with your existing pipeline.

---

## 💡 Example Command (GitHub Codespaces)
Run preprocessing anytime using:
```bash
python3 scripts/preprocess_sindhi.py
````

Output will appear at:

```
processed/cleaned_corpus.txt
```

---

## 🧑‍💻 Author Notes

This prompt context file allows consistent project scaling —
you can easily add NLP modules such as:

* Word frequency stats
* Lemmatization/tokenization
* Named Entity Recognition (NER)
* Topic modeling
* Vector embeddings
* Corpus visualizations

Just define the **🧭 EXTENSION GOAL** clearly below, and your assistant will handle the rest.
