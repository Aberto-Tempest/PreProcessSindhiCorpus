#!/usr/bin/env python3
"""
Sindhi Corpus Analysis Script
Analyzes both raw and cleaned Sindhi text with Unicode safety.
"""

import re
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display
import unicodedata
import os
import sys

# Add the parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SindhiCorpusAnalyzer:
    """Analyzer for Sindhi text corpora with RTL and Unicode support."""
    
    def __init__(self, output_dir="processed/analysis_outputs"):
        self.output_dir = output_dir
        self.ensure_output_dir()
        
        # Sindhi/Arabic Unicode ranges
        self.sindhi_chars = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
        self.sindhi_punctuation = r'[۔؟!]'
        
        # Configure matplotlib for RTL text
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['axes.unicode_minus'] = False
        
    def ensure_output_dir(self):
        """Create output directory if it doesn't exist."""
        os.makedirs(self.output_dir, exist_ok=True)
    
    def normalize_text(self, text):
        """Normalize Unicode text to NFC form for consistent joins."""
        return unicodedata.normalize('NFC', text)
    
    def prepare_rtl_text(self, text):
        """Prepare RTL text for visualization."""
        # Reshape Arabic script for proper display
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)
    
    def load_corpus(self, file_path):
        """Load corpus from file with UTF-8 encoding."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Warning: File {file_path} not found.")
            return ""
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return ""
    
    def extract_sindhi_words(self, text):
        """Extract Sindhi words from text, preserving Unicode joins."""
        # Normalize text first
        text = self.normalize_text(text)
        
        # Pattern to match Sindhi words (Sindhi/Arabic chars + possible diacritics)
        word_pattern = r'[' + self.sindhi_chars[2:-1] + r']+'
        words = re.findall(word_pattern, text)
        
        return [word for word in words if len(word) > 1]  # Filter single characters
    
    def calculate_corpus_statistics(self, text, corpus_name):
        """Calculate comprehensive corpus statistics."""
        words = self.extract_sindhi_words(text)
        sentences = self.split_sentences(text)
        
        stats = {
            'corpus_name': corpus_name,
            'total_characters': len(text),
            'total_words': len(words),
            'total_sentences': len(sentences),
            'unique_words': len(set(words)),
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
            'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
            'vocabulary_diversity': len(set(words)) / len(words) if words else 0
        }
        
        return stats, words, sentences
    
    def split_sentences(self, text):
        """Split text into sentences using Sindhi punctuation."""
        # Sindhi sentence boundaries: ۔ (Arabic full stop), ؟ (Arabic question mark), ! 
        sentences = re.split(r'[۔؟!]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def generate_word_frequency(self, words, top_n=50):
        """Generate word frequency analysis."""
        word_freq = Counter(words)
        return word_freq.most_common(top_n)
    
    def create_wordcloud(self, words, output_file):
        """Create a word cloud from Sindhi words."""
        try:
            # Combine words into text
            text = ' '.join(words)
            
            # Prepare text for RTL display
            prepared_text = self.prepare_rtl_text(text)
            
            # Configure word cloud for RTL
            wordcloud = WordCloud(
                font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Common font in Codespaces
                width=1200,
                height=800,
                background_color='white',
                max_words=200,
                colormap='viridis',
                prefer_horizontal=0.7  # Mix of horizontal and vertical for RTL
            ).generate(prepared_text)
            
            plt.figure(figsize=(15, 10))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(self.prepare_rtl_text('سندي لفظن جو بادل'), fontsize=16, pad=20)
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            print(f"Word cloud saved to: {output_file}")
            
        except Exception as e:
            print(f"Error creating word cloud: {e}")
            # Fallback: create a simple frequency visualization
            self.create_fallback_visualization(words, output_file)
    
    def create_fallback_visualization(self, words, output_file):
        """Create a fallback visualization if wordcloud fails."""
        word_freq = Counter(words)
        top_words = word_freq.most_common(20)
        
        if not top_words:
            return
            
        words_list, counts = zip(*top_words)
        prepared_words = [self.prepare_rtl_text(word) for word in words_list]
        
        plt.figure(figsize=(12, 8))
        bars = plt.barh(range(len(prepared_words)), counts)
        plt.yticks(range(len(prepared_words)), prepared_words)
        plt.xlabel('Frequency')
        plt.title(self.prepare_rtl_text('سندي لفظن جي فرقينس'))
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                    str(count), ha='left', va='center')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Fallback visualization saved to: {output_file}")
    
    def plot_frequency_distribution(self, word_freq, output_file, top_n=30):
        """Plot frequency distribution of top words."""
        if not word_freq:
            print("No word frequency data to plot.")
            return
            
        words, frequencies = zip(*word_freq[:top_n])
        prepared_words = [self.prepare_rtl_text(word) for word in words]
        
        plt.figure(figsize=(14, 8))
        bars = plt.bar(range(len(prepared_words)), frequencies, color='skyblue', alpha=0.7)
        
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.title(self.prepare_rtl_text(f'سڀ کان وڌيڪ استعمال ٿيندڙ {top_n} سندي لفظ'))
        plt.xticks(range(len(prepared_words)), prepared_words, rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, freq in zip(bars, frequencies):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(freq), ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Frequency distribution saved to: {output_file}")
    
    def save_word_frequency_csv(self, word_freq, output_file):
        """Save word frequency data to CSV."""
        df = pd.DataFrame(word_freq, columns=['word', 'frequency'])
        df['word_prepared'] = df['word'].apply(self.prepare_rtl_text)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Word frequency CSV saved to: {output_file}")
    
    def save_statistics_csv(self, stats_before, stats_after, output_file):
        """Save corpus statistics to CSV."""
        stats_df = pd.DataFrame([stats_before, stats_after])
        stats_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Corpus statistics saved to: {output_file}")
    
    def compare_corpora(self, raw_stats, cleaned_stats):
        """Generate comparison between raw and cleaned corpora."""
        comparison = {
            'metric': [
                'Total Words', 'Unique Words', 'Vocabulary Diversity',
                'Total Sentences', 'Average Sentence Length'
            ],
            'raw_corpus': [
                raw_stats['total_words'], raw_stats['unique_words'],
                raw_stats['vocabulary_diversity'], raw_stats['total_sentences'],
                raw_stats['avg_sentence_length']
            ],
            'cleaned_corpus': [
                cleaned_stats['total_words'], cleaned_stats['unique_words'],
                cleaned_stats['vocabulary_diversity'], cleaned_stats['total_sentences'],
                cleaned_stats['avg_sentence_length']
            ],
            'change_percent': [
                ((cleaned_stats['total_words'] - raw_stats['total_words']) / raw_stats['total_words'] * 100) if raw_stats['total_words'] > 0 else 0,
                ((cleaned_stats['unique_words'] - raw_stats['unique_words']) / raw_stats['unique_words'] * 100) if raw_stats['unique_words'] > 0 else 0,
                ((cleaned_stats['vocabulary_diversity'] - raw_stats['vocabulary_diversity']) / raw_stats['vocabulary_diversity'] * 100) if raw_stats['vocabulary_diversity'] > 0 else 0,
                ((cleaned_stats['total_sentences'] - raw_stats['total_sentences']) / raw_stats['total_sentences'] * 100) if raw_stats['total_sentences'] > 0 else 0,
                ((cleaned_stats['avg_sentence_length'] - raw_stats['avg_sentence_length']) / raw_stats['avg_sentence_length'] * 100) if raw_stats['avg_sentence_length'] > 0 else 0
            ]
        }
        return pd.DataFrame(comparison)
    
    def analyze_corpus(self, raw_corpus_path, cleaned_corpus_path):
        """Main analysis function for both raw and cleaned corpora."""
        print("Starting Sindhi corpus analysis...")
        
        # Load corpora
        raw_text = self.load_corpus(raw_corpus_path)
        cleaned_text = self.load_corpus(cleaned_corpus_path)
        
        if not raw_text and not cleaned_text:
            print("Error: Both corpora are empty. Analysis cannot proceed.")
            return
        
        # Calculate statistics
        print("Calculating corpus statistics...")
        raw_stats, raw_words, raw_sentences = self.calculate_corpus_statistics(raw_text, "raw_corpus")
        cleaned_stats, cleaned_words, cleaned_sentences = self.calculate_corpus_statistics(cleaned_text, "cleaned_corpus")
        
        # Generate word frequencies
        print("Generating word frequencies...")
        raw_word_freq = self.generate_word_frequency(raw_words)
        cleaned_word_freq = self.generate_word_frequency(cleaned_words)
        
        # Create visualizations for cleaned corpus
        print("Creating visualizations...")
        self.create_wordcloud(cleaned_words, os.path.join(self.output_dir, "wordcloud.png"))
        self.plot_frequency_distribution(cleaned_word_freq, 
                                       os.path.join(self.output_dir, "frequency_distribution.png"))
        
        # Save data files
        print("Saving analysis outputs...")
        self.save_word_frequency_csv(cleaned_word_freq, 
                                   os.path.join(self.output_dir, "word_frequency.csv"))
        self.save_statistics_csv(raw_stats, cleaned_stats, 
                               os.path.join(self.output_dir, "corpus_statistics.csv"))
        
        # Generate comparison
        comparison_df = self.compare_corpora(raw_stats, cleaned_stats)
        comparison_df.to_csv(os.path.join(self.output_dir, "corpus_comparison.csv"), 
                           index=False, encoding='utf-8')
        
        # Print summary
        self.print_analysis_summary(raw_stats, cleaned_stats)
        
        print("Analysis complete! Check the output directory for results.")
    
    def print_analysis_summary(self, raw_stats, cleaned_stats):
        """Print a summary of the analysis results."""
        print("\n" + "="*60)
        print("SINDHI CORPUS ANALYSIS SUMMARY")
        print("="*60)
        
        print(f"\n📊 CORPUS STATISTICS:")
        print(f"Raw Corpus:")
        print(f"  • Total Words: {raw_stats['total_words']:,}")
        print(f"  • Unique Words: {raw_stats['unique_words']:,}")
        print(f"  • Vocabulary Diversity: {raw_stats['vocabulary_diversity']:.3f}")
        print(f"  • Total Sentences: {raw_stats['total_sentences']:,}")
        
        print(f"\nCleaned Corpus:")
        print(f"  • Total Words: {cleaned_stats['total_words']:,}")
        print(f"  • Unique Words: {cleaned_stats['unique_words']:,}")
        print(f"  • Vocabulary Diversity: {cleaned_stats['vocabulary_diversity']:.3f}")
        print(f"  • Total Sentences: {cleaned_stats['total_sentences']:,}")
        
        # Calculate changes
        word_change = ((cleaned_stats['total_words'] - raw_stats['total_words']) / raw_stats['total_words']) * 100
        unique_change = ((cleaned_stats['unique_words'] - raw_stats['unique_words']) / raw_stats['unique_words']) * 100
        
        print(f"\n📈 CHANGES AFTER CLEANING:")
        print(f"  • Word Count Change: {word_change:+.1f}%")
        print(f"  • Unique Words Change: {unique_change:+.1f}%")
        print(f"  • Vocabulary Enrichment: {(cleaned_stats['vocabulary_diversity'] - raw_stats['vocabulary_diversity']):+.3f}")
        
        print(f"\n💾 OUTPUT FILES:")
        print(f"  • Word Cloud: {self.output_dir}/wordcloud.png")
        print(f"  • Frequency Distribution: {self.output_dir}/frequency_distribution.png")
        print(f"  • Word Frequency: {self.output_dir}/word_frequency.csv")
        print(f"  • Corpus Statistics: {self.output_dir}/corpus_statistics.csv")
        print(f"  • Corpus Comparison: {self.output_dir}/corpus_comparison.csv")
        print("="*60)

def main():
    """Main execution function."""
    # File paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_corpus_path = os.path.join(base_dir, "data", "raw_corpus.txt")
    cleaned_corpus_path = os.path.join(base_dir, "data", "cleaned_corpus.txt")
    output_dir = os.path.join(base_dir, "processed", "analysis_outputs")
    
    # Check if cleaned corpus exists
    if not os.path.exists(cleaned_corpus_path):
        print(f"Warning: Cleaned corpus not found at {cleaned_corpus_path}")
        print("Please run preprocess_sindhi.py first to generate cleaned_corpus.txt")
        
        # Check if raw corpus exists
        if not os.path.exists(raw_corpus_path):
            print(f"Error: Raw corpus not found at {raw_corpus_path}")
            print("Please ensure the data directory contains raw_corpus.txt")
            return
    
    # Initialize analyzer and run analysis
    analyzer = SindhiCorpusAnalyzer(output_dir)
    analyzer.analyze_corpus(raw_corpus_path, cleaned_corpus_path)

if __name__ == "__main__":
    # Install required packages if not available
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
    except ImportError:
        print("Installing required packages for RTL text support...")
        os.system("pip install arabic-reshaper python-bidi")
        
        # Retry imports
        import arabic_reshaper
        from bidi.algorithm import get_display
    
    main()