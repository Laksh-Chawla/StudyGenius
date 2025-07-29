"""
Action buttons widget for StudyGenius application.
Contains the main action buttons: Summarize, Generate Flashcards, Create Quiz.
"""

import sys
import os

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "src")
)

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFrame, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from src.utils.styles import AppStyles


class ActionButtonsWidget(QWidget):
    """Widget containing the main action buttons with responsive design."""

    summarize_clicked = pyqtSignal()
    flashcards_clicked = pyqtSignal()
    quiz_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.base_font_size = 14  # Increased from 11
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QHBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 10, 0, 10)

        # Create action buttons frame
        self.buttons_frame = QFrame()
        self.buttons_frame.setFrameStyle(QFrame.StyledPanel)
        self.buttons_frame.setStyleSheet(
            """
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
        """
        )

        frame_layout = QHBoxLayout(self.buttons_frame)
        frame_layout.setSpacing(20)

        # Summarize button
        self.summarize_button = self.create_action_button(
            "📄 Summarize", "Generate a concise summary of the text", "#28a745"  # Green
        )
        self.summarize_button.clicked.connect(self.summarize_clicked.emit)
        frame_layout.addWidget(self.summarize_button)

        # Generate Flashcards button
        self.flashcards_button = self.create_action_button(
            "🗂️ Generate Flashcards",
            "Create interactive flashcards for studying",
            "#007bff",  # Blue
        )
        self.flashcards_button.clicked.connect(self.flashcards_clicked.emit)
        frame_layout.addWidget(self.flashcards_button)

        # Create Quiz button
        self.quiz_button = self.create_action_button(
            "❓ Create Quiz", "Generate multiple choice questions", "#fd7e14"  # Orange
        )
        self.quiz_button.clicked.connect(self.quiz_clicked.emit)
        frame_layout.addWidget(self.quiz_button)

        layout.addWidget(self.buttons_frame)

    def create_action_button(self, text, tooltip, color):
        """Create a styled action button."""
        button = QPushButton(text)
        button.setFixedHeight(60)  # Increased from 50
        button.setMinimumWidth(200)  # Increased from 180
        button.setFont(QFont("Segoe UI", 14, QFont.Bold))  # Increased from 11
        button.setToolTip(tooltip)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Calculate hover and pressed colors
        hover_color = self.darken_color(color, 0.9)
        pressed_color = self.darken_color(color, 0.8)

        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 20px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                transform: translateY(-1px);
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
                transform: translateY(0px);
            }}
            QPushButton:disabled {{
                background-color: #e9ecef;
                color: #6c757d;
            }}
        """
        )

        return button

    def darken_color(self, hex_color, factor):
        """Darken a hex color by the given factor."""
        # Remove # if present
        hex_color = hex_color.lstrip("#")

        # Convert to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        # Darken
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)

        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"

    def set_buttons_enabled(self, enabled):
        """Enable or disable all action buttons."""
        self.summarize_button.setEnabled(enabled)
        self.flashcards_button.setEnabled(enabled)
        self.quiz_button.setEnabled(enabled)

    def update_fonts(self, window_width=1400, window_height=900):
        """Update font sizes based on window dimensions."""
        font_size = AppStyles.calculate_font_size(
            self.base_font_size, 1400, 900, window_width, window_height
        )

        # Update button fonts and styles
        button_font = QFont("Segoe UI", font_size, QFont.Bold)

        for button in [self.summarize_button, self.flashcards_button, self.quiz_button]:
            button.setFont(button_font)
            button.setFixedHeight(max(50, font_size * 4))
            button.setMinimumWidth(max(180, font_size * 15))
