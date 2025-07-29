"""
Quiz widget for StudyGenius application.
Displays multiple choice quiz questions with scoring.
"""

import sys
import os

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "src")
)

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QRadioButton,
    QButtonGroup,
    QFrame,
    QScrollArea,
    QProgressBar,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from src.utils.styles import AppStyles


class QuizWidget(QWidget):
    """Widget for displaying and taking quizzes with responsive design."""

    def __init__(self):
        super().__init__()
        self.questions = []
        self.current_question = 0
        self.user_answers = []
        self.quiz_completed = False
        self.base_font_size = 14  # Increased from 11
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel("❓ Quiz")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setStyleSheet("color: #333;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Progress info
        self.progress_label = QLabel("Question 0 of 0")
        self.progress_label.setStyleSheet("color: #666; font-size: 12px;")
        header_layout.addWidget(self.progress_label)

        layout.addLayout(header_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: none;
                background-color: #e9ecef;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 4px;
            }
        """
        )
        layout.addWidget(self.progress_bar)

        # Quiz content area
        self.quiz_frame = QFrame()
        self.quiz_frame.setFrameStyle(QFrame.StyledPanel)
        self.quiz_frame.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 25px;
            }
        """
        )

        self.quiz_layout = QVBoxLayout(self.quiz_frame)

        # Default content
        self.default_label = QLabel(
            "Click 'Create Quiz' to generate questions from your text"
        )
        self.default_label.setAlignment(Qt.AlignCenter)
        self.default_label.setFont(QFont("Segoe UI", 13))
        self.default_label.setStyleSheet("color: #666; padding: 50px;")
        self.quiz_layout.addWidget(self.default_label)

        layout.addWidget(self.quiz_frame)

        # Navigation controls
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(15)

        # Previous button
        self.prev_button = QPushButton("⬅️ Previous")
        self.prev_button.setFixedHeight(40)
        self.prev_button.setFixedWidth(120)
        self.prev_button.setStyleSheet(
            """
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:disabled {
                background-color: #e9ecef;
                color: #6c757d;
            }
        """
        )
        self.prev_button.clicked.connect(self.previous_question)
        self.prev_button.setEnabled(False)

        # Next/Submit button
        self.next_button = QPushButton("Next ➡️")
        self.next_button.setFixedHeight(40)
        self.next_button.setFixedWidth(120)
        self.next_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:disabled {
                background-color: #e9ecef;
                color: #6c757d;
            }
        """
        )
        self.next_button.clicked.connect(self.next_question)
        self.next_button.setEnabled(False)

        # Reset button
        self.reset_button = QPushButton("🔄 Reset Quiz")
        self.reset_button.setFixedHeight(40)
        self.reset_button.setFixedWidth(120)
        self.reset_button.setStyleSheet(
            """
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:disabled {
                background-color: #e9ecef;
                color: #6c757d;
            }
        """
        )
        self.reset_button.clicked.connect(self.reset_quiz)
        self.reset_button.setEnabled(False)

        nav_layout.addWidget(self.prev_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.reset_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_button)

        layout.addLayout(nav_layout)

    def set_questions(self, questions):
        """Set the quiz questions."""
        self.questions = questions
        self.current_question = 0
        self.user_answers = [-1] * len(questions)  # -1 means no answer selected
        self.quiz_completed = False

        if questions:
            self.default_label.hide()
            self.display_question()
            self.update_navigation()
            self.reset_button.setEnabled(True)
        else:
            self.default_label.show()
            self.progress_label.setText("Question 0 of 0")
            self.progress_bar.setValue(0)

    def display_question(self):
        """Display the current question."""
        if not self.questions or self.quiz_completed:
            return

        # Clear existing content
        for i in reversed(range(self.quiz_layout.count())):
            item = self.quiz_layout.itemAt(i)
            if item and item.widget() and item.widget() != self.default_label:
                item.widget().setParent(None)

        question_data = self.questions[self.current_question]

        # Question text
        question_label = QLabel(
            f"Q{self.current_question + 1}: {question_data['question']}"
        )
        question_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        question_label.setWordWrap(True)
        question_label.setStyleSheet("color: #333; margin-bottom: 15px; padding: 10px;")
        self.quiz_layout.addWidget(question_label)

        # Options
        self.option_group = QButtonGroup()

        for i, option in enumerate(question_data["options"]):
            radio = QRadioButton(f"{chr(65 + i)}. {option}")
            radio.setFont(QFont("Segoe UI", 11))
            radio.setStyleSheet(
                """
                QRadioButton {
                    color: #333;
                    padding: 8px;
                    spacing: 10px;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
                QRadioButton::indicator:unchecked {
                    border: 2px solid #ccc;
                    border-radius: 8px;
                    background-color: white;
                }
                QRadioButton::indicator:checked {
                    border: 2px solid #0078d4;
                    border-radius: 8px;
                    background-color: #0078d4;
                }
            """
            )

            # Check if this option was previously selected
            if self.user_answers[self.current_question] == i:
                radio.setChecked(True)

            radio.toggled.connect(
                lambda checked, idx=i: self.option_selected(idx, checked)
            )
            self.option_group.addButton(radio, i)
            self.quiz_layout.addWidget(radio)

        self.quiz_layout.addStretch()

        # Update progress
        self.progress_label.setText(
            f"Question {self.current_question + 1} of {len(self.questions)}"
        )
        progress_percent = ((self.current_question + 1) / len(self.questions)) * 100
        self.progress_bar.setValue(int(progress_percent))

    def option_selected(self, option_index, checked):
        """Handle option selection."""
        if checked:
            self.user_answers[self.current_question] = option_index
            self.update_navigation()

    def update_navigation(self):
        """Update navigation button states."""
        if not self.questions:
            return

        self.prev_button.setEnabled(self.current_question > 0)

        # Enable next button if an answer is selected
        has_answer = self.user_answers[self.current_question] != -1

        if self.current_question == len(self.questions) - 1:
            self.next_button.setText("✅ Submit Quiz")
            self.next_button.setEnabled(has_answer)
        else:
            self.next_button.setText("Next ➡️")
            self.next_button.setEnabled(has_answer)

    def previous_question(self):
        """Go to the previous question."""
        if self.current_question > 0:
            self.current_question -= 1
            self.display_question()
            self.update_navigation()

    def next_question(self):
        """Go to the next question or submit quiz."""
        if self.current_question == len(self.questions) - 1:
            self.submit_quiz()
        else:
            self.current_question += 1
            self.display_question()
            self.update_navigation()

    def submit_quiz(self):
        """Submit the quiz and show results."""
        self.quiz_completed = True

        # Calculate score
        correct_answers = 0
        for i, question in enumerate(self.questions):
            if self.user_answers[i] == question["correct"]:
                correct_answers += 1

        score_percentage = (correct_answers / len(self.questions)) * 100

        # Display results
        self.display_results(correct_answers, score_percentage)

    def display_results(self, correct_answers, score_percentage):
        """Display quiz results."""
        # Clear existing content
        for i in reversed(range(self.quiz_layout.count())):
            self.quiz_layout.itemAt(i).widget().setParent(None)

        # Results header
        results_label = QLabel("🎉 Quiz Complete!")
        results_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        results_label.setAlignment(Qt.AlignCenter)
        results_label.setStyleSheet("color: #28a745; margin-bottom: 20px;")
        self.quiz_layout.addWidget(results_label)

        # Score
        score_label = QLabel(
            f"Your Score: {correct_answers}/{len(self.questions)} ({score_percentage:.1f}%)"
        )
        score_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        score_label.setAlignment(Qt.AlignCenter)
        score_label.setStyleSheet("color: #333; margin-bottom: 15px;")
        self.quiz_layout.addWidget(score_label)

        # Performance message
        if score_percentage >= 90:
            message = "Excellent work! 🌟"
            color = "#28a745"
        elif score_percentage >= 70:
            message = "Good job! 👍"
            color = "#0078d4"
        elif score_percentage >= 50:
            message = "Not bad, but keep studying! 📚"
            color = "#fd7e14"
        else:
            message = "Keep practicing! 💪"
            color = "#dc3545"

        message_label = QLabel(message)
        message_label.setFont(QFont("Segoe UI", 12))
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setStyleSheet(f"color: {color}; margin-bottom: 20px;")
        self.quiz_layout.addWidget(message_label)

        self.quiz_layout.addStretch()

        # Update navigation
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)

    def reset_quiz(self):
        """Reset the quiz to start over."""
        if self.questions:
            self.current_question = 0
            self.user_answers = [-1] * len(self.questions)
            self.quiz_completed = False
            self.display_question()
            self.update_navigation()

    def update_fonts(self, window_width=1400, window_height=900):
        """Update font sizes based on window dimensions."""
        font_size = AppStyles.calculate_font_size(
            self.base_font_size, 1400, 900, window_width, window_height
        )

        # Update button fonts and sizes
        button_font = QFont("Segoe UI", font_size, QFont.Bold)
        button_height = max(45, font_size * 3)  # Increased minimum
        button_width = max(130, font_size * 10)  # Increased minimum

        for button in [self.prev_button, self.next_button, self.reset_button]:
            button.setFont(button_font)
            button.setFixedHeight(button_height)
            button.setFixedWidth(button_width)

        # Update label fonts
        title_font = QFont("Segoe UI", font_size + 3, QFont.Bold)  # Larger difference
        small_font = QFont("Segoe UI", max(12, font_size - 2))  # Minimum 12

        if hasattr(self, "title_label"):
            self.title_label.setFont(title_font)
        if hasattr(self, "progress_label"):
            self.progress_label.setFont(small_font)
        if hasattr(self, "default_label"):
            self.default_label.setFont(QFont("Segoe UI", font_size + 2))
