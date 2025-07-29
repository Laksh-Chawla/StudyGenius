"""
Example of how to integrate StudyGenius UI with your backend logic.
This shows how you can import and use the UI components in your main.py.
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui_main import StudyGeniusUI


def example_backend_integration():
    """Example showing how to connect backend logic to the UI."""

    app = QApplication(sys.argv)

    # Create the UI
    ui = StudyGeniusUI()

    # Connect your backend functions to UI signals
    ui.file_uploaded.connect(handle_file_upload)
    ui.summarize_requested.connect(handle_summarize_request)
    ui.flashcards_requested.connect(handle_flashcards_request)
    ui.quiz_requested.connect(handle_quiz_request)

    # Show the UI
    ui.show()

    return app.exec_()


def handle_file_upload(file_path, content):
    """Handle file upload from UI."""
    print(f"Backend received file: {file_path}")
    print(f"Content length: {len(content)} characters")
    # Add your file processing logic here


def handle_summarize_request(text):
    """Handle summarization request from UI."""
    print(f"Backend received summarize request for {len(text)} characters")

    # Example: Call your AI summarization service
    # summary = your_ai_service.summarize(text)

    # For now, just create a mock summary
    summary = f"This is a summary of the {len(text.split())} word text."

    # You can display the summary by calling UI methods
    # ui.display_summary(summary)
    print(f"Generated summary: {summary}")


def handle_flashcards_request(text):
    """Handle flashcards generation request from UI."""
    print(f"Backend received flashcards request for {len(text)} characters")

    # Example: Call your AI flashcard generation service
    # flashcards = your_ai_service.generate_flashcards(text)

    # For now, create mock flashcards
    words = text.split()[:10]  # Take first 10 words
    flashcards = [
        {"front": f"What is {word}?", "back": f"Definition of {word}"} for word in words
    ]

    # You can display flashcards by calling UI methods
    # ui.display_flashcards(flashcards)
    print(f"Generated {len(flashcards)} flashcards")


def handle_quiz_request(text):
    """Handle quiz generation request from UI."""
    print(f"Backend received quiz request for {len(text)} characters")

    # Example: Call your AI quiz generation service
    # quiz_questions = your_ai_service.generate_quiz(text)

    # For now, create mock quiz questions
    words = text.split()[:5]  # Take first 5 words
    quiz_questions = []

    for i, word in enumerate(words):
        question = {
            "question": f"Which word appears in position {i+1}?",
            "options": [word, "incorrect1", "incorrect2", "incorrect3"],
            "correct": 0,
        }
        quiz_questions.append(question)

    # You can display quiz by calling UI methods
    # ui.display_quiz(quiz_questions)
    print(f"Generated {len(quiz_questions)} quiz questions")


if __name__ == "__main__":
    """
    This is how you would use the UI in your main.py:

    1. Import the StudyGeniusUI class
    2. Create an instance
    3. Connect your backend functions to the UI signals
    4. Show the UI and run the application
    """
    sys.exit(example_backend_integration())
