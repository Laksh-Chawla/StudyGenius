"""
Text display widget for StudyGenius application.
Provides a large text area for viewing and editing content.
"""

import sys
import os

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "src")
)

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QFrame,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from src.utils.styles import AppStyles


class TextDisplayWidget(QWidget):
    """Widget for displaying and editing text content with responsive design."""

    text_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.base_font_size = 14  # Increased from 11
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel("📝 Document Content")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title_label.setStyleSheet("color: #333;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Word count label
        self.word_count_label = QLabel("0 words")
        self.word_count_label.setStyleSheet("color: #666; font-size: 11px;")
        header_layout.addWidget(self.word_count_label)

        layout.addLayout(header_layout)

        # Text edit area
        self.text_edit = QTextEdit()
        self.text_edit.setMinimumHeight(300)
        self.text_edit.setMaximumHeight(400)
        self.text_edit.setPlaceholderText("Upload a file or paste your text here...")
        self.update_fonts()

        # Connect text changed signal
        self.text_edit.textChanged.connect(self.on_text_changed)

        layout.addWidget(self.text_edit)

        # Footer with text actions
        footer_layout = QHBoxLayout()

        # Clear text button
        self.clear_button = QPushButton("Clear Text")
        self.clear_button.setFixedHeight(30)
        self.clear_button.setStyleSheet(
            """
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
            QPushButton:disabled {
                background-color: #e9ecef;
                color: #6c757d;
            }
        """
        )
        self.clear_button.clicked.connect(self.clear_text)
        self.clear_button.setEnabled(False)

        # Copy text button
        self.copy_button = QPushButton("Copy All")
        self.copy_button.setFixedHeight(30)
        self.copy_button.setStyleSheet(
            """
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
            QPushButton:pressed {
                background-color: #117a8b;
            }
            QPushButton:disabled {
                background-color: #e9ecef;
                color: #6c757d;
            }
        """
        )
        self.copy_button.clicked.connect(self.copy_text)
        self.copy_button.setEnabled(False)

        footer_layout.addWidget(self.clear_button)
        footer_layout.addWidget(self.copy_button)
        footer_layout.addStretch()

        layout.addLayout(footer_layout)

    def on_text_changed(self):
        """Handle text changes."""
        text = self.text_edit.toPlainText()
        word_count = len(text.split()) if text.strip() else 0
        self.word_count_label.setText(f"{word_count} words")

        # Enable/disable buttons based on content
        has_text = bool(text.strip())
        self.clear_button.setEnabled(has_text)
        self.copy_button.setEnabled(has_text)

        # Emit signal
        self.text_changed.emit(text)

    def set_text(self, text):
        """Set the text content."""
        self.text_edit.setPlainText(text)

    def get_text(self):
        """Get the current text content."""
        return self.text_edit.toPlainText()

    def clear_text(self):
        """Clear all text."""
        self.text_edit.clear()

    def copy_text(self):
        """Copy all text to clipboard."""
        self.text_edit.selectAll()
        self.text_edit.copy()

    def update_fonts(self, window_width=1400, window_height=900):
        """Update font sizes based on window dimensions."""
        font_size = AppStyles.calculate_font_size(
            self.base_font_size, 1400, 900, window_width, window_height
        )

        # Update text edit font and style
        text_font = QFont("Segoe UI", font_size)
        self.text_edit.setFont(text_font)
        self.text_edit.setStyleSheet(AppStyles.get_responsive_text_style(font_size))

        # Update header labels
        if hasattr(self, "title_label"):
            title_font = QFont(
                "Segoe UI", font_size + 3, QFont.Bold
            )  # Larger difference
            self.title_label.setFont(title_font)

        if hasattr(self, "word_count_label"):
            count_font = QFont("Segoe UI", max(12, font_size - 2))  # Minimum 12
            self.word_count_label.setFont(count_font)
