"""
Insights widget for StudyGenius application.
Displays study metrics, difficulty rating, and time estimates.
"""

import os
import sys

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "src")
)

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QProgressBar,
    QHBoxLayout,
    QGroupBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.utils.styles import AppStyles


class InsightsWidget(QWidget):
    """Widget for displaying study insights and analytics with responsive design."""

    def __init__(self):
        super().__init__()
        self.base_font_size = 14  # Increased from 12
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(5, 0, 5, 0)

        # Title
        self.title_label = QLabel("📊 Study Insights")
        self.title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))  # Increased from 16
        self.title_label.setStyleSheet("color: #333; margin-bottom: 10px;")
        layout.addWidget(self.title_label)

        # File Information Group
        self.file_info_group = self.create_info_group("📄 File Information")
        layout.addWidget(self.file_info_group)

        # Text Statistics Group
        self.text_stats_group = self.create_info_group("📝 Text Statistics")
        layout.addWidget(self.text_stats_group)

        # Study Metrics Group
        self.study_metrics_group = self.create_info_group("⏱️ Study Metrics")
        layout.addWidget(self.study_metrics_group)

        # Difficulty Assessment Group
        self.difficulty_group = self.create_info_group("🎯 Difficulty Rating")
        layout.addWidget(self.difficulty_group)

        layout.addStretch()

    def create_info_group(self, title):
        """Create a styled information group."""
        group = QGroupBox(title)
        group.setFont(QFont("Segoe UI", 10, QFont.Bold))
        group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #f8f9fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: #495057;
                background-color: transparent;
            }
        """
        )

        layout = QVBoxLayout(group)
        layout.setSpacing(8)

        if title == "📄 File Information":
            self.file_name_label = QLabel("No file loaded")
            self.file_size_label = QLabel("Size: --")
            self.file_type_label = QLabel("Type: --")

            for label in [
                self.file_name_label,
                self.file_size_label,
                self.file_type_label,
            ]:
                label.setFont(QFont("Segoe UI", 12))
                label.setStyleSheet("color: #495057; padding: 4px 0px;")

            layout.addWidget(self.file_name_label)
            layout.addWidget(self.file_size_label)
            layout.addWidget(self.file_type_label)

        elif title == "📝 Text Statistics":
            self.word_count_label = QLabel("Words: 0")
            self.char_count_label = QLabel("Characters: 0")
            self.reading_level_label = QLabel("Reading Level: --")

            for label in [
                self.word_count_label,
                self.char_count_label,
                self.reading_level_label,
            ]:
                label.setFont(QFont("Segoe UI", 12))
                label.setStyleSheet("color: #495057; padding: 4px 0px;")

            layout.addWidget(self.word_count_label)
            layout.addWidget(self.char_count_label)
            layout.addWidget(self.reading_level_label)

        elif title == "⏱️ Study Metrics":
            self.est_reading_time_label = QLabel("Reading Time: --")
            self.est_study_time_label = QLabel("Study Time: --")
            self.flashcard_count_label = QLabel("Potential Cards: --")

            for label in [
                self.est_reading_time_label,
                self.est_study_time_label,
                self.flashcard_count_label,
            ]:
                label.setFont(QFont("Segoe UI", 12))
                label.setStyleSheet("color: #495057; padding: 4px 0px;")

            layout.addWidget(self.est_reading_time_label)
            layout.addWidget(self.est_study_time_label)
            layout.addWidget(self.flashcard_count_label)

        elif title == "🎯 Difficulty Rating":
            self.difficulty_label = QLabel("Assessment: --")
            self.difficulty_label.setFont(QFont("Segoe UI", 12))
            self.difficulty_label.setStyleSheet("color: #495057; padding: 4px 0px;")
            layout.addWidget(self.difficulty_label)

            # Difficulty progress bar
            self.difficulty_bar = QProgressBar()
            self.difficulty_bar.setFixedHeight(25)  # Increased from 20
            self.difficulty_bar.setTextVisible(False)
            self.difficulty_bar.setStyleSheet(
                """
                QProgressBar {
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    background-color: #f0f0f0;
                }
                QProgressBar::chunk {
                    border-radius: 9px;
                }
            """
            )
            layout.addWidget(self.difficulty_bar)

            self.difficulty_desc_label = QLabel(
                "Difficulty level will be calculated based on text complexity"
            )
            self.difficulty_desc_label.setWordWrap(True)
            self.difficulty_desc_label.setFont(QFont("Segoe UI", 10))
            self.difficulty_desc_label.setStyleSheet("color: #666; padding: 4px 0px;")
            layout.addWidget(self.difficulty_desc_label)

        # Labels already have proper fonts set above
        return group

    def update_file_info(self, file_path, content_length):
        """Update file information display."""
        if not file_path:
            self.file_name_label.setText("No file loaded")
            self.file_size_label.setText("Size: --")
            self.file_type_label.setText("Type: --")
            return

        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_ext = os.path.splitext(file_path)[1].upper().replace(".", "")

        # Format file size
        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"

        self.file_name_label.setText(f"📄 {filename}")
        self.file_size_label.setText(f"Size: {size_str}")
        self.file_type_label.setText(f"Type: {file_ext}")

    def update_text_stats(self, word_count, text):
        """Update text statistics display."""
        char_count = len(text)
        char_count_no_spaces = len(text.replace(" ", ""))

        self.word_count_label.setText(f"Words: {word_count:,}")
        self.char_count_label.setText(f"Characters: {char_count:,}")

        # Calculate basic reading level (simplified)
        if word_count > 0:
            avg_word_length = char_count_no_spaces / word_count
            if avg_word_length < 4:
                reading_level = "Elementary"
            elif avg_word_length < 5:
                reading_level = "Middle School"
            elif avg_word_length < 6:
                reading_level = "High School"
            else:
                reading_level = "College"
        else:
            reading_level = "--"

        self.reading_level_label.setText(f"Reading Level: {reading_level}")

        # Update study metrics
        self.update_study_metrics(word_count, text)

        # Update difficulty assessment
        self.update_difficulty_assessment(word_count, text)

    def update_study_metrics(self, word_count, text):
        """Update study time estimates."""
        if word_count == 0:
            self.est_reading_time_label.setText("Reading Time: --")
            self.est_study_time_label.setText("Study Time: --")
            self.flashcard_count_label.setText("Potential Cards: --")
            return

        # Estimate reading time (average 200 words per minute)
        reading_minutes = word_count / 200
        if reading_minutes < 1:
            reading_time = f"{reading_minutes * 60:.0f} seconds"
        elif reading_minutes < 60:
            reading_time = f"{reading_minutes:.1f} minutes"
        else:
            hours = reading_minutes / 60
            reading_time = f"{hours:.1f} hours"

        # Estimate study time (3x reading time for thorough study)
        study_minutes = reading_minutes * 3
        if study_minutes < 60:
            study_time = f"{study_minutes:.1f} minutes"
        else:
            study_hours = study_minutes / 60
            study_time = f"{study_hours:.1f} hours"

        # Estimate potential flashcards (rough estimate: 1 card per 50-100 words)
        potential_cards = word_count // 75

        self.est_reading_time_label.setText(f"Reading Time: {reading_time}")
        self.est_study_time_label.setText(f"Study Time: {study_time}")
        self.flashcard_count_label.setText(f"Potential Cards: ~{potential_cards}")

    def update_difficulty_assessment(self, word_count, text):
        """Update difficulty assessment."""
        if word_count == 0:
            self.difficulty_label.setText("Assessment: --")
            self.difficulty_bar.setValue(0)
            self.difficulty_bar.setStyleSheet(
                """
                QProgressBar {
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    background-color: #f0f0f0;
                }
                QProgressBar::chunk {
                    border-radius: 9px;
                    background-color: #e9ecef;
                }
            """
            )
            return

        # Simple difficulty calculation based on text characteristics
        difficulty_score = 0

        # Factor 1: Average word length
        words = text.split()
        avg_word_length = sum(len(word.strip('.,!?;:"()[]{}')) for word in words) / len(
            words
        )
        if avg_word_length > 6:
            difficulty_score += 30
        elif avg_word_length > 5:
            difficulty_score += 20
        elif avg_word_length > 4:
            difficulty_score += 10

        # Factor 2: Sentence complexity (approximate by counting punctuation)
        sentences = text.count(".") + text.count("!") + text.count("?")
        if sentences > 0:
            avg_sentence_length = word_count / sentences
            if avg_sentence_length > 20:
                difficulty_score += 25
            elif avg_sentence_length > 15:
                difficulty_score += 15
            elif avg_sentence_length > 10:
                difficulty_score += 5

        # Factor 3: Vocabulary complexity (count of longer words)
        complex_words = sum(1 for word in words if len(word.strip('.,!?;:"()[]{}')) > 7)
        complex_ratio = complex_words / word_count if word_count > 0 else 0
        if complex_ratio > 0.2:
            difficulty_score += 25
        elif complex_ratio > 0.1:
            difficulty_score += 15
        elif complex_ratio > 0.05:
            difficulty_score += 10

        # Factor 4: Text length
        if word_count > 2000:
            difficulty_score += 20
        elif word_count > 1000:
            difficulty_score += 10
        elif word_count > 500:
            difficulty_score += 5

        # Normalize score to 0-100
        difficulty_score = min(100, difficulty_score)

        # Determine difficulty level and color
        if difficulty_score < 25:
            level = "Easy"
            color = "#28a745"  # Green
        elif difficulty_score < 50:
            level = "Moderate"
            color = "#ffc107"  # Yellow
        elif difficulty_score < 75:
            level = "Challenging"
            color = "#fd7e14"  # Orange
        else:
            level = "Difficult"
            color = "#dc3545"  # Red

        self.difficulty_label.setText(f"Assessment: {level}")
        self.difficulty_bar.setValue(difficulty_score)
        self.difficulty_bar.setStyleSheet(
            f"""
            QProgressBar {{
                border: 1px solid #ccc;
                border-radius: 10px;
                background-color: #f0f0f0;
            }}
            QProgressBar::chunk {{
                border-radius: 9px;
                background-color: {color};
            }}
        """
        )

    def update_fonts(self, window_width=1400, window_height=900):
        """Update font sizes based on window dimensions."""
        font_size = AppStyles.calculate_font_size(
            self.base_font_size, 1400, 900, window_width, window_height
        )

        # Update title font
        title_font = QFont(
            "Segoe UI", font_size + 4, QFont.Bold
        )  # Even larger difference
        self.title_label.setFont(title_font)

        # Update all insight labels with larger fonts
        label_font = QFont("Segoe UI", font_size + 2)  # Larger base font
        small_font = QFont("Segoe UI", max(11, font_size))  # Increased minimum

        # Update all specific labels directly
        labels_to_update = [
            self.file_name_label,
            self.file_size_label,
            self.file_type_label,
            self.word_count_label,
            self.char_count_label,
            self.reading_level_label,
            self.est_reading_time_label,
            self.est_study_time_label,
            self.flashcard_count_label,
            self.difficulty_label,
        ]

        for label in labels_to_update:
            label.setFont(label_font)

        # Update description label
        self.difficulty_desc_label.setFont(QFont("Segoe UI", max(10, font_size - 1)))

        # Update group box styling with larger fonts
        group_font_size = font_size + 1
        for group in [
            self.file_info_group,
            self.text_stats_group,
            self.study_metrics_group,
            self.difficulty_group,
        ]:
            group.setStyleSheet(
                f"""
                QGroupBox {{
                    font-weight: bold;
                    border: 1px solid #dee2e6;
                    border-radius: 6px;
                    margin-top: {max(8, group_font_size//2)}px;
                    padding-top: {max(8, group_font_size//2)}px;
                    background-color: #f8f9fa;
                    font-size: {group_font_size}px;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    padding: 0 {max(8, group_font_size//2)}px;
                    color: #495057;
                    background-color: transparent;
                }}
            """
            )
