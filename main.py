#!/usr/bin/env python3
"""
StudyGenius Main Application
Integrates UI with text processing, flashcard generation, and quiz creation.
"""

import sys
import os
import random
import traceback
from pathlib import Path

# Add src and UI directories to Python path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir / "src"))
sys.path.append(str(current_dir / "UI"))

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import pyqtSignal
from UI.ui_main import StudyGeniusUI
from src.textTransformer import TextTransformer
from src.flashCard import FlashCardGenerator
from src.quiz import QuizGenerator


class StudyGeniusApp:
    """Main application class that coordinates UI and backend processing."""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ui = StudyGeniusUI()

        # Initialize backend processors
        self.text_transformer = TextTransformer()
        self.flashcard_generator = FlashCardGenerator()
        self.quiz_generator = QuizGenerator()

        # Setup connections
        self.setup_connections()

    def setup_connections(self):
        """Setup signal-slot connections between UI and backend."""

        # File upload handling - override the default behavior
        self.ui.file_uploaded.connect(self.handle_file_upload)

        # Action button handling - override the default behavior
        self.ui.flashcards_requested.connect(self.handle_flashcards_request)
        self.ui.quiz_requested.connect(self.handle_quiz_request)

    def handle_file_upload(self, file_path, content):
        """Handle file upload - extract text if needed and update text display."""
        if not file_path or not file_path.strip():
            return

        try:
            file_extension = Path(file_path).suffix.lower()

            # If it's a PDF or TXT file, extract text using textTransformer
            if file_extension in [".pdf", ".txt"]:
                self.ui.set_status_message("Extracting text from file...")
                self.app.processEvents()  # Allow UI to update

                extracted_text = self.text_transformer.transform_file(file_path)
                if extracted_text:
                    # Update the text display with extracted content
                    self.ui.text_display_widget.set_text(extracted_text)
                    self.ui.set_status_message(
                        f"Text extracted from {Path(file_path).name}"
                    )
                else:
                    self.show_error(
                        "Could not extract text from file. Please check file format."
                    )
                    self.ui.set_status_message("Text extraction failed")
            else:
                # For other files, the content should already be processed by the UI
                self.ui.set_status_message(f"File loaded: {Path(file_path).name}")

        except Exception as e:
            error_msg = f"Error processing file: {str(e)}"
            self.show_error(error_msg)
            self.ui.set_status_message("File processing failed")

    def handle_flashcards_request(self, text):
        """Handle request to generate flashcards."""
        if not text or not text.strip():
            self.show_error("No text available to generate flashcards from.")
            return

        try:
            self.ui.set_status_message("Generating flashcards...")
            self.app.processEvents()  # Allow UI to update

            if len(text.strip()) < 50:
                self.show_error("Text is too short to generate meaningful flashcards.")
                self.ui.set_status_message("Ready")
                return

            flashcards = self.flashcard_generator.generate_flashcards(
                text, num_cards=10
            )

            if flashcards and len(flashcards) > 0:
                # Convert flashcard format from [question, answer] to dictionary format for UI
                formatted_flashcards = []
                for flashcard in flashcards:
                    if isinstance(flashcard, list) and len(flashcard) >= 2:
                        front, back = flashcard[0], flashcard[1]
                        formatted_card = {"front": str(front), "back": str(back)}
                        formatted_flashcards.append(formatted_card)
                    else:
                        print(f"Invalid flashcard format: {flashcard}")

                if formatted_flashcards:
                    self.ui.display_flashcards(formatted_flashcards)
                    self.ui.set_status_message(
                        f"{len(formatted_flashcards)} flashcards generated"
                    )
                else:
                    self.show_error("Could not format flashcards properly.")
                    self.ui.set_status_message("Flashcard formatting failed")
            else:
                self.show_error("Could not generate flashcards from the provided text.")
                self.ui.set_status_message("Flashcard generation failed")

        except Exception as e:
            error_msg = f"Error generating flashcards: {str(e)}"
            print(f"Flashcard error details: {e}")  # Debug print
            traceback.print_exc()  # Debug traceback
            self.show_error(error_msg)
            self.ui.set_status_message("Flashcard generation failed")

    def handle_quiz_request(self, text):
        """Handle request to generate quiz."""
        if not text or not text.strip():
            self.show_error("No text available to generate quiz from.")
            return

        try:
            self.ui.set_status_message("Generating quiz questions...")
            self.app.processEvents()  # Allow UI to update

            if len(text.strip()) < 50:
                self.show_error(
                    "Text is too short to generate meaningful quiz questions."
                )
                self.ui.set_status_message("Ready")
                return

            quiz_questions = self.quiz_generator.generate_quiz(text, num_questions=10)

            if quiz_questions and len(quiz_questions) > 0:
                # Convert quiz format from [question, answer] to dictionary format for UI
                formatted_questions = []
                for quiz_item in quiz_questions:
                    if isinstance(quiz_item, list) and len(quiz_item) >= 2:
                        question, answer = quiz_item[0], quiz_item[1]

                        # Create multiple choice options with the correct answer and some better distractors
                        options = [str(answer)]

                        # Create more sensible distractors based on context
                        answer_words = str(answer).lower().split()

                        # Generate context-aware distractors
                        context_distractors = []

                        # If answer is a single word, create variations
                        if len(answer_words) == 1:
                            base_word = answer_words[0]
                            # Add some domain-specific alternatives
                            if "learning" in base_word or "machine" in base_word:
                                context_distractors.extend(
                                    [
                                        "Deep learning",
                                        "Supervised learning",
                                        "Neural networks",
                                    ]
                                )
                            elif "data" in base_word:
                                context_distractors.extend(
                                    ["Information", "Statistics", "Database"]
                                )
                            elif "network" in base_word:
                                context_distractors.extend(
                                    ["Algorithm", "Model", "System"]
                                )
                            elif "algorithm" in base_word:
                                context_distractors.extend(
                                    ["Method", "Process", "Technique"]
                                )

                        # Add some general smart distractors
                        general_distractors = [
                            "Artificial intelligence",
                            "Data processing",
                            "Statistical analysis",
                            "Pattern recognition",
                            "Computer science",
                            "Information technology",
                            "None of the above",
                            "Cannot be determined",
                        ]

                        # Combine and filter distractors
                        all_distractors = context_distractors + general_distractors

                        # Add distractors until we have 4 options total, ensuring they're different from the answer
                        for distractor in all_distractors:
                            if (
                                len(options) < 4
                                and distractor.lower() != str(answer).lower()
                            ):
                                # Avoid very similar distractors
                                if not any(
                                    distractor.lower() in existing.lower()
                                    or existing.lower() in distractor.lower()
                                    for existing in options
                                ):
                                    options.append(distractor)

                        # If we still don't have enough options, add generic ones
                        if len(options) < 4:
                            final_distractors = [
                                "Not mentioned in the text",
                                "All of the above",
                                "Insufficient data",
                            ]
                            for distractor in final_distractors:
                                if len(options) < 4 and distractor not in options:
                                    options.append(distractor)

                        # Shuffle options so correct answer isn't always first
                        random.shuffle(options)
                        correct_index = options.index(str(answer))

                        formatted_question = {
                            "question": str(question),
                            "options": options,
                            "correct_answer": correct_index,
                        }
                        formatted_questions.append(formatted_question)
                    else:
                        print(f"Invalid quiz format: {quiz_item}")

                if formatted_questions:
                    self.ui.display_quiz(formatted_questions)
                    self.ui.set_status_message(
                        f"{len(formatted_questions)} quiz questions generated"
                    )
                else:
                    self.show_error("Could not format quiz questions properly.")
                    self.ui.set_status_message("Quiz formatting failed")
            else:
                self.show_error(
                    "Could not generate quiz questions from the provided text."
                )
                self.ui.set_status_message("Quiz generation failed")

        except Exception as e:
            error_msg = f"Error generating quiz: {str(e)}"
            print(f"Quiz error details: {e}")  # Debug print
            traceback.print_exc()  # Debug traceback
            self.show_error(error_msg)
            self.ui.set_status_message("Quiz generation failed")

    def show_error(self, message):
        """Show error message to user."""
        QMessageBox.warning(self.ui, "StudyGenius", message)

    def run(self):
        """Run the application."""
        try:
            self.ui.show()
            return self.app.exec_()
        except Exception as e:
            self.show_error(f"Application error: {str(e)}")
            return 1


def main():
    """Main entry point."""
    try:
        # Create and run the application
        app = StudyGeniusApp()
        sys.exit(app.run())
    except Exception as e:
        print(f"Failed to start StudyGenius: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
