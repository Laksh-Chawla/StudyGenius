import re
import random
import nltk
from typing import List, Tuple, Optional, Dict
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


class QuizGenerator:
    """
    A class to generate quiz questions from text using sumy and NLP techniques.
    Returns questions as a list where each element is [question, answer].
    """

    def __init__(self, language: str = "english"):
        """
        Initialize the Quiz generator.

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
        self, text: str, num_sentences: int = 15, summarizer_type: str = "lsa"
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

    def create_what_questions(self, sentences: List[str]) -> List[Tuple[str, str]]:
        what_questions = []

        for sentence in sentences:
            sentence = sentence.strip()
            words = sentence.split()

            if len(words) < 6:
                continue

            is_match = re.search(r"([A-Z][a-zA-Z\s]+?)\s+is\s+([^.!?]+)", sentence)
            if is_match:
                subject = is_match.group(1).strip()
                definition = is_match.group(2).strip()
                question = f"What is {subject}?"
                what_questions.append((question, definition))
                continue

            refers_match = re.search(
                r"([A-Z][a-zA-Z\s]+?)\s+refers to\s+([^.!?]+)", sentence
            )
            if refers_match:
                subject = refers_match.group(1).strip()
                definition = refers_match.group(2).strip()
                question = f"What does {subject} refer to?"
                what_questions.append((question, definition))
                continue

            means_match = re.search(
                r"([A-Z][a-zA-Z\s]+?)\s+means\s+([^.!?]+)", sentence
            )
            if means_match:
                subject = means_match.group(1).strip()
                definition = means_match.group(2).strip()
                question = f"What does {subject} mean?"
                what_questions.append((question, definition))
                continue

            if any(word.istitle() for word in words[:4]):
                subject_words = []
                for word in words[:4]:
                    if word.istitle() or word.isupper():
                        subject_words.append(word)
                    elif subject_words:
                        break

                if subject_words and len(subject_words) <= 3:
                    subject = " ".join(subject_words)
                    question = f"What is {subject}?"
                    what_questions.append((question, sentence))

        return what_questions

    def create_how_questions(self, sentences: List[str]) -> List[Tuple[str, str]]:
        how_questions = []

        process_keywords = [
            "process",
            "method",
            "way",
            "procedure",
            "algorithm",
            "technique",
            "approach",
        ]
        action_words = [
            "works",
            "functions",
            "operates",
            "performs",
            "executes",
            "processes",
        ]

        for sentence in sentences:
            sentence = sentence.strip()
            sentence_lower = sentence.lower()

            if len(sentence.split()) < 6:
                continue

            for keyword in process_keywords:
                if keyword in sentence_lower:
                    question = f"How does the {keyword} work?"
                    how_questions.append((question, sentence))
                    break

            for action in action_words:
                if action in sentence_lower:
                    action_index = sentence_lower.find(action)
                    words_before = sentence[:action_index].split()
                    if words_before:
                        subject = " ".join(words_before[-3:]).strip()
                        question = f"How does {subject} {action}?"
                        how_questions.append((question, sentence))
                        break

            if " by " in sentence_lower:
                parts = sentence.split(" by ")
                if len(parts) >= 2:
                    main_part = parts[0].strip()
                    method_part = parts[1].strip()
                    question = f"How is {main_part.lower()} achieved?"
                    how_questions.append((question, f"By {method_part}"))

        return how_questions

    def create_why_questions(self, sentences: List[str]) -> List[Tuple[str, str]]:
        why_questions = []

        reason_keywords = [
            "because",
            "since",
            "due to",
            "as a result",
            "therefore",
            "consequently",
            "thus",
        ]
        purpose_keywords = ["in order to", "to", "for", "purpose", "goal", "aim"]

        for sentence in sentences:
            sentence = sentence.strip()
            sentence_lower = sentence.lower()

            if len(sentence.split()) < 6:
                continue

            for keyword in reason_keywords:
                if keyword in sentence_lower:
                    parts = re.split(rf"\b{keyword}\b", sentence, flags=re.IGNORECASE)
                    if len(parts) >= 2:
                        effect = parts[0].strip()
                        reason = parts[1].strip()
                        if effect and reason:
                            question = f"Why {effect.lower()}?"
                            why_questions.append((question, f"Because {reason}"))
                    break

            for keyword in purpose_keywords:
                if keyword in sentence_lower:
                    if keyword == "to" and sentence_lower.count(" to ") == 1:
                        parts = sentence.split(" to ")
                        if len(parts) == 2:
                            action = parts[0].strip()
                            purpose = parts[1].strip()
                            question = f"Why {action.lower()}?"
                            why_questions.append((question, f"To {purpose}"))
                    break

        return why_questions

    def create_when_questions(self, sentences: List[str]) -> List[Tuple[str, str]]:
        when_questions = []

        time_patterns = [
            r"\b(in \d{4})\b",
            r"\b(during [^,\.]+)\b",
            r"\b(after [^,\.]+)\b",
            r"\b(before [^,\.]+)\b",
            r"\b(when [^,\.]+)\b",
            r"\b(since \d{4})\b",
        ]

        for sentence in sentences:
            sentence = sentence.strip()

            if len(sentence.split()) < 6:
                continue

            for pattern in time_patterns:
                matches = re.findall(pattern, sentence, re.IGNORECASE)
                if matches:
                    time_info = matches[0]
                    question_part = re.sub(
                        pattern, "", sentence, flags=re.IGNORECASE
                    ).strip()
                    question_part = re.sub(r"\s+", " ", question_part)

                    if question_part:
                        question = f"When {question_part.lower()}?"
                        when_questions.append((question, time_info))
                    break

        return when_questions

    def create_where_questions(self, sentences: List[str]) -> List[Tuple[str, str]]:
        where_questions = []

        location_patterns = [
            r"\b(in [A-Z][a-zA-Z\s]+)\b",
            r"\b(at [A-Z][a-zA-Z\s]+)\b",
            r"\b(on [A-Z][a-zA-Z\s]+)\b",
            r"\b(within [^,\.]+)\b",
            r"\b(throughout [^,\.]+)\b",
        ]

        for sentence in sentences:
            sentence = sentence.strip()

            if len(sentence.split()) < 6:
                continue

            for pattern in location_patterns:
                matches = re.findall(pattern, sentence, re.IGNORECASE)
                if matches:
                    location_info = matches[0]
                    question_part = re.sub(
                        pattern, "", sentence, flags=re.IGNORECASE
                    ).strip()
                    question_part = re.sub(r"\s+", " ", question_part)

                    if question_part:
                        question = f"Where {question_part.lower()}?"
                        where_questions.append((question, location_info))
                    break

        return where_questions

    def create_fill_in_blank_questions(
        self, sentences: List[str]
    ) -> List[Tuple[str, str]]:
        fill_questions = []

        for sentence in sentences:
            sentence = sentence.strip()
            words = sentence.split()

            if len(words) < 8:
                continue

            important_word_indices = []
            for i, word in enumerate(words):
                if (
                    len(word) > 4
                    and word.lower() not in self.stop_words
                    and word.isalpha()
                    and not word.lower()
                    in ["this", "that", "they", "them", "their", "there"]
                ):
                    important_word_indices.append(i)

            if important_word_indices:
                blank_index = random.choice(important_word_indices)
                answer = words[blank_index]

                question_words = words.copy()
                question_words[blank_index] = "______"
                question = "Fill in the blank: " + " ".join(question_words)

                fill_questions.append((question, answer))

        return fill_questions

    def create_true_false_questions(
        self, sentences: List[str]
    ) -> List[Tuple[str, str]]:
        tf_questions = []

        for sentence in sentences:
            sentence = sentence.strip()
            words = sentence.split()

            if len(words) < 6:
                continue

            true_question = f"True or False: {sentence}"
            tf_questions.append((true_question, "True"))

            modified_sentence = self._modify_sentence_for_false(sentence)
            if modified_sentence and modified_sentence != sentence:
                false_question = f"True or False: {modified_sentence}"
                tf_questions.append((false_question, "False"))

        return tf_questions

    def _modify_sentence_for_false(self, sentence: str) -> Optional[str]:
        modifications = [
            ("is", "is not"),
            ("are", "are not"),
            ("can", "cannot"),
            ("will", "will not"),
            ("does", "does not"),
            ("has", "has not"),
            ("have", "have not"),
        ]

        sentence_lower = sentence.lower()
        for original, replacement in modifications:
            if f" {original} " in sentence_lower:
                return sentence.replace(f" {original} ", f" {replacement} ")

        return None

    def generate_quiz(self, text: str, num_questions: int = 10) -> List[List[str]]:
        if not text or len(text.strip()) < 50:
            return []

        key_sentences = self.extract_key_sentences(
            text, num_sentences=max(20, num_questions * 2)
        )

        if not key_sentences:
            return []

        all_questions = []

        question_generators = [
            self.create_what_questions,
            self.create_how_questions,
            self.create_why_questions,
            self.create_when_questions,
            self.create_where_questions,
            self.create_fill_in_blank_questions,
            self.create_true_false_questions,
        ]

        for generator in question_generators:
            try:
                questions = generator(key_sentences)
                all_questions.extend(questions)
            except Exception as e:
                continue

        seen_questions = set()
        unique_questions = []
        for q, a in all_questions:
            if q not in seen_questions:
                seen_questions.add(q)
                unique_questions.append([q, a])

        random.shuffle(unique_questions)
        return unique_questions[:num_questions]

    def format_quiz(self, quiz_questions: List[List[str]]) -> str:
        if not quiz_questions:
            return "No quiz questions could be generated from the provided text."

        formatted = "Generated Quiz Questions:\n" + "=" * 50 + "\n\n"

        for i, question_answer in enumerate(quiz_questions, 1):
            question, answer = question_answer
            formatted += f"Question {i}:\n"
            formatted += f"{question}\n"
            formatted += f"Answer: {answer}\n"
            formatted += "-" * 30 + "\n\n"

        return formatted


def main():
    generator = QuizGenerator()

    sample_text = """
    Artificial Intelligence is a branch of computer science that aims to create intelligent machines 
    that can think and learn like humans. Machine Learning is a subset of AI that enables computers 
    to learn without being explicitly programmed. Deep Learning uses neural networks with multiple 
    layers to model and understand complex patterns in data. Natural Language Processing helps 
    computers understand and interpret human language. AI has applications in many fields including 
    healthcare, finance, and transportation. The goal of AI is to create systems that can perform 
    tasks that typically require human intelligence.
    """

    print("Quiz Generator - Create quiz questions from text using sumy")
    print(
        "Supported question types: What, How, Why, When, Where, Fill-in-blank, True/False"
    )

    quiz_questions = generator.generate_quiz(sample_text, num_questions=10)
    print(generator.format_quiz(quiz_questions))


if __name__ == "__main__":
    main()
