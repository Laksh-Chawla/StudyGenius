#!/usr/bin/env python3
"""
StudyGenius Text Summarizer
Uses Sumy library to generate intelligent text summaries with multiple algorithms.
"""

import re
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextSummarizer:
    """
    Advanced text summarization using multiple Sumy algorithms.
    Provides different summarization strategies for various use cases.
    """

    def __init__(self, language="english"):
        """
        Initialize the summarizer with a specific language.

        Args:
            language (str): Language for tokenization and stop words (default: "english")
        """
        self.language = language
        self.stemmer = Stemmer(language)
        self.stop_words = get_stop_words(language)

        # Download required NLTK data
        self._ensure_nltk_data()

    def _ensure_nltk_data(self):
        """Download required NLTK data if not already present."""
        try:
            nltk.data.find("tokenizers/punkt_tab")
        except LookupError:
            logger.info("Downloading NLTK punkt_tab tokenizer...")
            nltk.download("punkt_tab", quiet=True)

        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            logger.info("Downloading NLTK punkt tokenizer...")
            nltk.download("punkt", quiet=True)

        try:
            nltk.data.find("corpora/stopwords")
        except LookupError:
            logger.info("Downloading NLTK stopwords...")
            nltk.download("stopwords", quiet=True)

    def _preprocess_text(self, text):
        if not text or not text.strip():
            return ""

        text = re.sub(r"\s+", " ", text)
        text = re.sub(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            "",
            text,
        )
        text = re.sub(r"\S+@\S+", "", text)
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def _calculate_sentence_count(self, text, summary_ratio=0.3):
        sentence_count = len(re.findall(r"[.!?]+", text))
        summary_sentences = max(1, min(10, int(sentence_count * summary_ratio)))
        return summary_sentences

    def summarize_lsa(self, text, sentence_count=None, summary_ratio=0.3):
        try:
            text = self._preprocess_text(text)
            if not text:
                return "Error: No valid text to summarize."

            parser = PlaintextParser.from_string(text, Tokenizer(self.language))
            summarizer = LsaSummarizer(self.stemmer)
            summarizer.stop_words = self.stop_words

            if sentence_count is None:
                sentence_count = self._calculate_sentence_count(text, summary_ratio)

            summary = summarizer(parser.document, sentence_count)
            return " ".join([str(sentence) for sentence in summary])

        except Exception as e:
            logger.error(f"LSA summarization failed: {str(e)}")
            return f"Error: Failed to generate LSA summary - {str(e)}"

    def summarize_luhn(self, text, sentence_count=None, summary_ratio=0.3):
        try:
            text = self._preprocess_text(text)
            if not text:
                return "Error: No valid text to summarize."

            parser = PlaintextParser.from_string(text, Tokenizer(self.language))
            summarizer = LuhnSummarizer(self.stemmer)
            summarizer.stop_words = self.stop_words

            if sentence_count is None:
                sentence_count = self._calculate_sentence_count(text, summary_ratio)

            summary = summarizer(parser.document, sentence_count)
            return " ".join([str(sentence) for sentence in summary])

        except Exception as e:
            logger.error(f"Luhn summarization failed: {str(e)}")
            return f"Error: Failed to generate Luhn summary - {str(e)}"

    def summarize_textrank(self, text, sentence_count=None, summary_ratio=0.3):
        try:
            text = self._preprocess_text(text)
            if not text:
                return "Error: No valid text to summarize."

            parser = PlaintextParser.from_string(text, Tokenizer(self.language))
            summarizer = TextRankSummarizer(self.stemmer)
            summarizer.stop_words = self.stop_words

            if sentence_count is None:
                sentence_count = self._calculate_sentence_count(text, summary_ratio)

            summary = summarizer(parser.document, sentence_count)
            return " ".join([str(sentence) for sentence in summary])

        except Exception as e:
            logger.error(f"TextRank summarization failed: {str(e)}")
            return f"Error: Failed to generate TextRank summary - {str(e)}"

    def summarize_lexrank(self, text, sentence_count=None, summary_ratio=0.3):
        """
        Summarize text using LexRank algorithm.
        Good for news articles and narrative texts.

        Args:
            text (str): Input text to summarize
            sentence_count (int, optional): Number of sentences in summary
            summary_ratio (float): Ratio of original text to include

        Returns:
            str: Summarized text
        """
        try:
            text = self._preprocess_text(text)
            if not text:
                return "Error: No valid text to summarize."

            parser = PlaintextParser.from_string(text, Tokenizer(self.language))
            summarizer = LexRankSummarizer(self.stemmer)
            summarizer.stop_words = self.stop_words

            if sentence_count is None:
                sentence_count = self._calculate_sentence_count(text, summary_ratio)

            summary = summarizer(parser.document, sentence_count)
            return " ".join([str(sentence) for sentence in summary])

        except Exception as e:
            logger.error(f"LexRank summarization failed: {str(e)}")
            return f"Error: Failed to generate LexRank summary - {str(e)}"

    def summarize_edmundson(self, text, sentence_count=None, summary_ratio=0.3):
        """
        Summarize text using Edmundson algorithm.
        Good for structured documents with clear topics.

        Args:
            text (str): Input text to summarize
            sentence_count (int, optional): Number of sentences in summary
            summary_ratio (float): Ratio of original text to include

        Returns:
            str: Summarized text
        """
        try:
            text = self._preprocess_text(text)
            if not text:
                return "Error: No valid text to summarize."

            parser = PlaintextParser.from_string(text, Tokenizer(self.language))
            summarizer = EdmundsonSummarizer(self.stemmer)
            summarizer.stop_words = self.stop_words

            if sentence_count is None:
                sentence_count = self._calculate_sentence_count(text, summary_ratio)

            summary = summarizer(parser.document, sentence_count)
            return " ".join([str(sentence) for sentence in summary])

        except Exception as e:
            logger.error(f"Edmundson summarization failed: {str(e)}")
            return f"Error: Failed to generate Edmundson summary - {str(e)}"

    def summarize_auto(self, text, sentence_count=None, summary_ratio=0.3):
        """
        Automatically choose the best summarization algorithm and generate summary.
        Tries multiple algorithms and returns the best result.

        Args:
            text (str): Input text to summarize
            sentence_count (int, optional): Number of sentences in summary
            summary_ratio (float): Ratio of original text to include

        Returns:
            dict: Summary results with algorithm used and summary text
        """
        text = self._preprocess_text(text)
        if not text:
            return {
                "algorithm": "none",
                "summary": "Error: No valid text to summarize.",
                "success": False,
            }

        # Try different algorithms in order of preference
        algorithms = [
            ("TextRank", self.summarize_textrank),
            ("LSA", self.summarize_lsa),
            ("LexRank", self.summarize_lexrank),
            ("Luhn", self.summarize_luhn),
        ]

        for name, method in algorithms:
            try:
                summary = method(text, sentence_count, summary_ratio)
                if summary and not summary.startswith("Error:"):
                    return {"algorithm": name, "summary": summary, "success": True}
            except Exception as e:
                logger.warning(f"{name} algorithm failed: {str(e)}")
                continue

        return {
            "algorithm": "fallback",
            "summary": "Error: All summarization algorithms failed.",
            "success": False,
        }

    def get_summary_stats(self, original_text, summary_text):
        if not original_text or not summary_text:
            return {}

        original_words = len(original_text.split())
        summary_words = len(summary_text.split())
        original_chars = len(original_text)
        summary_chars = len(summary_text)

        compression_ratio = (
            (summary_words / original_words) * 100 if original_words > 0 else 0
        )

        return {
            "original_words": original_words,
            "summary_words": summary_words,
            "original_characters": original_chars,
            "summary_characters": summary_chars,
            "compression_ratio": round(compression_ratio, 1),
            "reduction_percentage": round(100 - compression_ratio, 1),
        }


def quick_summarize(text, algorithm="auto", sentence_count=None, summary_ratio=0.3):
    summarizer = TextSummarizer()

    if algorithm == "auto":
        result = summarizer.summarize_auto(text, sentence_count, summary_ratio)
        return result["summary"]
    elif algorithm == "textrank":
        return summarizer.summarize_textrank(text, sentence_count, summary_ratio)
    elif algorithm == "lsa":
        return summarizer.summarize_lsa(text, sentence_count, summary_ratio)
    elif algorithm == "lexrank":
        return summarizer.summarize_lexrank(text, sentence_count, summary_ratio)
    elif algorithm == "luhn":
        return summarizer.summarize_luhn(text, sentence_count, summary_ratio)
    elif algorithm == "edmundson":
        return summarizer.summarize_edmundson(text, sentence_count, summary_ratio)
    else:
        return "Error: Unknown algorithm. Use 'auto', 'textrank', 'lsa', 'lexrank', 'luhn', or 'edmundson'."


if __name__ == "__main__":
    # Example usage
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural 
    intelligence displayed by humans and animals. Leading AI textbooks define the field as the study 
    of "intelligent agents": any device that perceives its environment and takes actions that maximize 
    its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" 
    is often used to describe machines that mimic "cognitive" functions that humans associate with the 
    human mind, such as "learning" and "problem solving". As machines become increasingly capable, 
    tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon 
    known as the AI effect. A quip in Tesler's Theorem says "AI is whatever hasn't been done yet." 
    For instance, optical character recognition is frequently excluded from things considered to be AI, 
    having become a routine technology. Modern machine learning techniques are a core part of AI. 
    Machine learning algorithms build a model based on sample data, known as "training data", in order 
    to make predictions or decisions without being explicitly programmed to do so.
    """

    print("=== StudyGenius Text Summarizer Demo ===\n")

    summarizer = TextSummarizer()

    # Test different algorithms
    print("1. Auto Summary:")
    auto_result = summarizer.summarize_auto(sample_text)
    print(f"Algorithm used: {auto_result['algorithm']}")
    print(f"Summary: {auto_result['summary']}\n")

    print("2. TextRank Summary:")
    textrank_summary = summarizer.summarize_textrank(sample_text)
    print(f"Summary: {textrank_summary}\n")

    print("3. Summary Statistics:")
    stats = summarizer.get_summary_stats(sample_text, auto_result["summary"])
    for key, value in stats.items():
        print(f"{key}: {value}")
