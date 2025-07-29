import re
import nltk
from typing import List, Tuple, Optional
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import random


class FlashCardGenerator:
    """
    A class to generate flashcards from text using sumy for summarization.
    Returns flashcards as a list where each element is [question/keyword, answer/meaning].
    """

    def __init__(self, language: str = "english"):
        """
        Initialize the FlashCard generator.

        Args:
            language: Language for text processing (default: "english")
        """
        self.language = language
        self.stemmer = Stemmer(language)
        self.stop_words = get_stop_words(language)

        # Download required NLTK data
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt")

        try:
            nltk.data.find("tokenizers/punkt_tab")
        except LookupError:
            nltk.download("punkt_tab")

    def clean_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w\s.,!?;:-]", "", text)
        return text.strip()

    def extract_key_sentences(
        self, text: str, num_sentences: int = 10, summarizer_type: str = "lsa"
    ) -> List[str]:
        cleaned_text = self.clean_text(text)
        parser = PlaintextParser.from_string(cleaned_text, Tokenizer(self.language))

        if summarizer_type.lower() == "luhn":
            summarizer = LuhnSummarizer(self.stemmer)
        elif summarizer_type.lower() == "textrank":
            summarizer = TextRankSummarizer(self.stemmer)
        else:
            summarizer = LsaSummarizer(self.stemmer)

        summarizer.stop_words = self.stop_words
        summary_sentences = summarizer(parser.document, num_sentences)

        return [str(sentence) for sentence in summary_sentences]

    def extract_keywords_and_definitions(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract potential keywords and their definitions from text.

        Args:
            text: Input text

        Returns:
            List[Tuple[str, str]]: List of (keyword, definition) pairs
        """
        keyword_patterns = [
            # Pattern: "Term is/means/refers to definition"
            r"([A-Z][a-zA-Z\s]+?)\s+(?:is|are|means|refers to|defined as)\s+([^.!?]+[.!?])",
            # Pattern: "Definition: explanation"
            r"([A-Z][a-zA-Z\s]+?):\s+([^.!?]+[.!?])",
            # Pattern: "Term - definition"
            r"([A-Z][a-zA-Z\s]+?)\s*[-–—]\s*([^.!?]+[.!?])",
            # Pattern: "Term (definition)"
            r"([A-Z][a-zA-Z\s]+?)\s*\(([^)]+)\)",
        ]

        keyword_definitions = []

        for pattern in keyword_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                keyword = match.group(1).strip()
                definition = match.group(2).strip()

                # Clean up keyword and definition
                keyword = re.sub(r"^[Tt]he\s+", "", keyword)  # Remove "The" at start
                definition = definition.rstrip(".,!?")  # Remove trailing punctuation

                # Ensure definition starts with uppercase
                if definition and definition[0].islower():
                    definition = definition[0].upper() + definition[1:]

                # Filter out very short or very long keywords/definitions
                if (
                    1 <= len(keyword.split()) <= 4
                    and 3 <= len(definition.split()) <= 30
                    and not keyword.lower()
                    in ["this", "that", "these", "those", "it", "they"]
                ):
                    # Make it more natural - create a proper definition
                    clean_definition = definition
                    if not any(
                        word in definition.lower()
                        for word in ["is", "are", "refers", "means"]
                    ):
                        # Add connecting words to make it flow better
                        if keyword.endswith("s"):
                            clean_definition = f"are {definition.lower()}"
                        else:
                            clean_definition = f"is {definition.lower()}"

                    keyword_definitions.append((keyword, clean_definition))

        return keyword_definitions

    def create_question_answer_pairs(
        self, sentences: List[str]
    ) -> List[Tuple[str, str]]:
        """
        Create question-answer pairs from sentences.

        Args:
            sentences: List of key sentences

        Returns:
            List[Tuple[str, str]]: List of (question, answer) pairs
        """
        qa_pairs = []

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence.split()) < 5:  # Skip very short sentences
                continue

            # Create different types of questions
            question_types = [
                self._create_what_question(sentence),
                self._create_why_question(sentence),
                self._create_how_question(sentence),
                self._create_when_question(sentence),
                self._create_where_question(sentence),
            ]

            # Choose a random question type that's not None
            valid_questions = [q for q in question_types if q is not None]
            if valid_questions:
                question, answer = random.choice(valid_questions)
                qa_pairs.append((question, answer))

        return qa_pairs

    def _create_what_question(self, sentence: str) -> Optional[Tuple[str, str]]:
        """Create a 'What is...' type question."""
        sentence = sentence.strip()

        # Look for definition patterns
        if " is " in sentence or " are " in sentence:
            parts = re.split(r"\s+(?:is|are)\s+", sentence, 1, re.IGNORECASE)
            if len(parts) == 2:
                subject = parts[0].strip()
                definition = parts[1].strip()

                # Clean up the subject and definition
                subject = re.sub(r"^[Tt]he\s+", "", subject)  # Remove "The" at start
                definition = definition.rstrip(".")  # Remove trailing period

                if len(subject.split()) <= 5 and len(definition.split()) >= 3:
                    question = f"What is {subject}?"
                    return (question, definition)

        # Look for concepts mentioned in the sentence
        words = sentence.split()
        if len(words) > 8:
            # Find potential key terms (capitalized words or technical terms)
            key_terms = [word for word in words if word[0].isupper() and len(word) > 3]
            if key_terms:
                term = key_terms[0]
                question = f"What is {term}?"
                # Use the sentence as context for the answer
                clean_answer = sentence.rstrip(".")
                return (question, clean_answer)

        return None

    def _create_why_question(self, sentence: str) -> Optional[Tuple[str, str]]:
        """Create a 'Why...' type question."""
        sentence = sentence.strip()

        # Look for causal relationships
        causal_patterns = [
            (r"\bbecause\b", "because"),
            (r"\bsince\b", "since"),
            (r"\bdue to\b", "due to"),
            (r"\bas a result of\b", "as a result of"),
            (r"\btherefore\b", "therefore"),
            (r"\bconsequently\b", "consequently"),
        ]

        for pattern, keyword in causal_patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                # Split on the causal word
                parts = re.split(pattern, sentence, 1, re.IGNORECASE)
                if len(parts) == 2:
                    effect = parts[0].strip().rstrip(",.")
                    cause = parts[1].strip()

                    if len(effect.split()) >= 3 and len(cause.split()) >= 3:
                        question = f"Why {effect.lower()}?"
                        answer = f"Because {cause.lower().rstrip('.')}"
                        return (question, answer)

        return None

    def _create_how_question(self, sentence: str) -> Optional[Tuple[str, str]]:
        """Create a 'How...' type question."""
        sentence = sentence.strip()

        # Look for process or method descriptions
        process_keywords = [
            "process",
            "method",
            "way",
            "procedure",
            "technique",
            "approach",
            "algorithm",
        ]

        for keyword in process_keywords:
            if keyword in sentence.lower():
                # Create a question about the process
                if "work" in sentence.lower() or "function" in sentence.lower():
                    # Extract the main subject
                    words = sentence.split()
                    if len(words) > 6:
                        # Find the main subject (usually near the beginning)
                        subject_words = []
                        for word in words[:5]:
                            if word.lower() not in ["the", "a", "an", "this", "that"]:
                                subject_words.append(word)
                            if len(subject_words) >= 2:
                                break

                        if subject_words:
                            subject = " ".join(subject_words).rstrip(",.")
                            question = f"How does {subject.lower()} work?"
                            answer = sentence.rstrip(".")
                            return (question, answer)

        return None

    def _create_when_question(self, sentence: str) -> Optional[Tuple[str, str]]:
        """Create a 'When...' type question."""
        sentence = sentence.strip()

        # Look for time-related information
        time_patterns = [
            r"\b(?:in|during|at|on|when|after|before)\s+\d+",  # Years, dates
            r"\b(?:in|during)\s+the\s+\w+",  # "in the past", "during the process"
            r"\bwhen\s+\w+",  # "when something happens"
        ]

        for pattern in time_patterns:
            matches = re.search(pattern, sentence, re.IGNORECASE)
            if matches:
                # Extract the temporal context
                time_phrase = matches.group()
                rest_of_sentence = sentence.replace(matches.group(), "").strip()

                if len(rest_of_sentence.split()) >= 4:
                    question = f"When {rest_of_sentence.lower().rstrip('.')}?"
                    answer = time_phrase
                    return (question, answer)

        return None

    def _create_where_question(self, sentence: str) -> Optional[Tuple[str, str]]:
        """Create a 'Where...' type question."""
        sentence = sentence.strip()

        # Look for explicit location information
        location_patterns = [
            r"\bin\s+(?:the\s+)?(\w+(?:\s+\w+)?)\s+(?:field|domain|area|industry)",
            r"\bat\s+(\w+(?:\s+\w+)?)",
            r"\bwithin\s+(\w+(?:\s+\w+)?)",
        ]

        for pattern in location_patterns:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                location = match.group(1)
                # Extract what is being located
                words = sentence.split()
                main_subject = []
                for word in words[:5]:  # Look at first few words
                    clean_word = word.strip(".,!?:;")
                    if clean_word[0].isupper() and clean_word.lower() not in [
                        "the",
                        "in",
                        "at",
                        "this",
                    ]:
                        main_subject.append(clean_word)

                if main_subject and len(main_subject) <= 2:
                    subject = " ".join(main_subject)
                    question = f"Where is {subject} commonly used?"
                    answer = f"In {location}"
                    return (question, answer)

        # If no explicit location found, skip this type of question
        return None

    def generate_flashcards(
        self, text: str, num_cards: int = 10, card_types: List[str] = None
    ) -> List[List[str]]:
        """
        Generate flashcards from text.

        Args:
            text: Input text to generate flashcards from
            num_cards: Maximum number of flashcards to generate
            card_types: Types of cards to generate ["qa", "keyword"] (default: both)

        Returns:
            List[List[str]]: List of flashcards, each as [question/keyword, answer/meaning]
        """
        if card_types is None:
            card_types = ["qa", "keyword"]

        flashcards = []

        # Generate keyword-definition cards
        if "keyword" in card_types:
            keyword_defs = self.extract_keywords_and_definitions(text)
            for keyword, definition in keyword_defs[: num_cards // 2]:
                flashcards.append([keyword, definition])

        # Generate question-answer cards
        if "qa" in card_types:
            key_sentences = self.extract_key_sentences(text, num_sentences=num_cards)
            qa_pairs = self.create_question_answer_pairs(key_sentences)

            remaining_slots = num_cards - len(flashcards)
            for question, answer in qa_pairs[:remaining_slots]:
                flashcards.append([question, answer])

        if len(flashcards) < num_cards:
            key_sentences = self.extract_key_sentences(
                text, num_sentences=num_cards * 2
            )
            remaining_slots = num_cards - len(flashcards)

            for sentence in key_sentences[:remaining_slots]:
                if len(sentence.split()) > 8:
                    words = sentence.split()
                    if len(words) > 6:
                        key_word_candidates = []

                        for i, word in enumerate(words):
                            clean_word = word.strip(".,!?:;")
                            if (
                                clean_word
                                and clean_word[0].isupper()
                                and len(clean_word) > 3
                            ):
                                if clean_word.lower() not in [
                                    "the",
                                    "this",
                                    "that",
                                    "these",
                                    "those",
                                ]:
                                    key_word_candidates.append((i, clean_word))
                            elif len(clean_word) > 6 and clean_word.lower() not in [
                                "the",
                                "and",
                                "but",
                                "or",
                                "however",
                                "therefore",
                            ]:
                                key_word_candidates.append((i, clean_word))

                        if key_word_candidates:
                            # Choose the first good candidate
                            word_index, key_word = key_word_candidates[0]
                            question_words = words.copy()
                            question_words[word_index] = "______"

                            # Create a more natural question format
                            question_text = " ".join(question_words).rstrip(".")
                            question = f"Complete the sentence: {question_text}"

                            # Clean up the answer
                            clean_answer = key_word.strip(".,!?:;")
                            flashcards.append([question, clean_answer])
                        else:
                            # Fallback: use middle word if no good candidates found
                            word_index = len(words) // 2
                            key_word = words[word_index].strip(".,!?:;")
                            question_words = words.copy()
                            question_words[word_index] = "______"
                            question = f"Complete the sentence: {' '.join(question_words).rstrip('.')}"
                            flashcards.append([question, key_word])

        # Shuffle the flashcards for variety
        random.shuffle(flashcards)

        return flashcards[:num_cards]

    def format_flashcards(self, flashcards: List[List[str]]) -> str:
        formatted = "Generated Flashcards:\n" + "=" * 50 + "\n\n"

        for i, card in enumerate(flashcards, 1):
            formatted += f"Card {i}:\n"
            formatted += f"Q: {card[0]}\n"
            formatted += f"A: {card[1]}\n"
            formatted += "-" * 30 + "\n\n"

        return formatted


def main():
    generator = FlashCardGenerator()

    sample_text = """
    Artificial Intelligence is a branch of computer science that aims to create intelligent machines.
    Machine Learning is a subset of AI that enables computers to learn without being explicitly programmed.
    Deep Learning uses neural networks with multiple layers to model and understand complex patterns.
    Natural Language Processing helps computers understand and interpret human language.
    """

    print("FlashCard Generator - Create flashcards from text using sumy")
    print("Supported card types: question-answer pairs and keyword-definition pairs")

    flashcards = generator.generate_flashcards(sample_text, num_cards=5)
    print(generator.format_flashcards(flashcards))


if __name__ == "__main__":
    main()
