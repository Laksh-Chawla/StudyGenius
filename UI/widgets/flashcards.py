"""
Flashcards widget for StudyGenius application.
Displays flashcards with front/back content and navigation controls.
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
    QFrame,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from src.utils.styles import AppStyles


class FlashcardsWidget(QWidget):
    """Widget for displaying and navigating flashcards with responsive design."""

    def __init__(self):
        super().__init__()
        self.flashcards = []
        self.current_index = 0
        self.showing_front = True
        self.base_font_size = 14  # Increased from 11
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel("🗂️ Flashcards")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setStyleSheet("color: #333;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Counter label
        self.counter_label = QLabel("0 / 0")
        self.counter_label.setStyleSheet("color: #666; font-size: 12px;")
        header_layout.addWidget(self.counter_label)

        layout.addLayout(header_layout)

        # Flashcard display area
        self.card_frame = QFrame()
        self.card_frame.setMinimumHeight(500)  # Increased from 250 to 500 (2x height)
        self.card_frame.setFrameStyle(QFrame.StyledPanel)
        self.card_frame.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                padding: 30px;
            }
            QFrame:hover {
                border-color: #0078d4;
            }
        """
        )

        card_layout = QVBoxLayout(self.card_frame)
        card_layout.setAlignment(Qt.AlignCenter)

        # Side indicator (Front/Back)
        self.side_label = QLabel("Front")
        self.side_label.setAlignment(Qt.AlignCenter)
        self.side_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.side_label.setStyleSheet(
            """
            QLabel {
                color: #0078d4;
                background-color: #e6f3ff;
                border-radius: 12px;
                padding: 4px 12px;
                margin-bottom: 10px;
            }
        """
        )
        self.side_label.setFixedHeight(24)
        self.side_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        card_layout.addWidget(self.side_label, alignment=Qt.AlignCenter)

        # Card content
        self.content_label = QLabel("Click 'Generate Flashcards' to create study cards")
        self.content_label.setAlignment(Qt.AlignCenter)
        self.content_label.setFont(QFont("Segoe UI", 13))
        self.content_label.setWordWrap(True)
        self.content_label.setStyleSheet(
            """
            QLabel {
                color: #333;
                line-height: 1.5;
                background: transparent;
                border: none;
                padding: 20px;
            }
        """
        )
        card_layout.addWidget(self.content_label)

        # Flip hint
        self.flip_hint = QLabel("💡 Click on the card to flip")
        self.flip_hint.setAlignment(Qt.AlignCenter)
        self.flip_hint.setFont(QFont("Segoe UI", 10))
        self.flip_hint.setStyleSheet(
            "color: #999; background: transparent; border: none;"
        )
        card_layout.addWidget(self.flip_hint)

        # Make card clickable
        self.card_frame.mousePressEvent = self.flip_card

        layout.addWidget(self.card_frame)

        # Navigation controls
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(20)

        # Previous button
        self.prev_button = QPushButton("⬅️ Previous")
        self.prev_button.setFixedHeight(40)
        self.prev_button.setFixedWidth(120)
        self.prev_button.setFont(QFont("Segoe UI", 10))
        self.prev_button.setStyleSheet(
            """
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
            }
            QPushButton:disabled {
                background-color: #e9ecef;
                color: #6c757d;
            }
        """
        )
        self.prev_button.clicked.connect(self.previous_card)
        self.prev_button.setEnabled(False)

        # Flip button
        self.flip_button = QPushButton("🔄 Flip Card")
        self.flip_button.setFixedHeight(40)
        self.flip_button.setFixedWidth(120)
        self.flip_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.flip_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #e9ecef;
                color: #6c757d;
            }
        """
        )
        self.flip_button.clicked.connect(self.flip_card)
        self.flip_button.setEnabled(False)

        # Next button
        self.next_button = QPushButton("Next ➡️")
        self.next_button.setFixedHeight(40)
        self.next_button.setFixedWidth(120)
        self.next_button.setFont(QFont("Segoe UI", 10))
        self.next_button.setStyleSheet(
            """
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton:disabled {
                background-color: #e9ecef;
                color: #6c757d;
            }
        """
        )
        self.next_button.clicked.connect(self.next_card)
        self.next_button.setEnabled(False)

        nav_layout.addStretch()
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.flip_button)
        nav_layout.addWidget(self.next_button)
        nav_layout.addStretch()

        layout.addLayout(nav_layout)

    def set_flashcards(self, flashcards):
        """Set the flashcards data."""
        self.flashcards = flashcards
        self.current_index = 0
        self.showing_front = True

        if flashcards:
            self.update_display()
            self.update_navigation()
            self.flip_button.setEnabled(True)
            self.flip_hint.show()
        else:
            self.content_label.setText("No flashcards available")
            self.counter_label.setText("0 / 0")
            self.flip_button.setEnabled(False)
            self.flip_hint.hide()

    def update_display(self):
        """Update the flashcard display."""
        if not self.flashcards:
            return

        card = self.flashcards[self.current_index]

        if self.showing_front:
            self.side_label.setText("Front")
            self.content_label.setText(card["front"])
            self.side_label.setStyleSheet(
                """
                QLabel {
                    color: #0078d4;
                    background-color: #e6f3ff;
                    border-radius: 12px;
                    padding: 4px 12px;
                }
            """
            )
        else:
            self.side_label.setText("Back")
            self.content_label.setText(card["back"])
            self.side_label.setStyleSheet(
                """
                QLabel {
                    color: #28a745;
                    background-color: #e6f7e6;
                    border-radius: 12px;
                    padding: 4px 12px;
                }
            """
            )

        self.counter_label.setText(f"{self.current_index + 1} / {len(self.flashcards)}")

    def update_navigation(self):
        """Update navigation button states."""
        if not self.flashcards:
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
            return

        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < len(self.flashcards) - 1)

    def flip_card(self, event=None):
        """Flip the current card."""
        if not self.flashcards:
            return

        self.showing_front = not self.showing_front
        self.update_display()

    def previous_card(self):
        """Go to the previous card."""
        if self.current_index > 0:
            self.current_index -= 1
            self.showing_front = True
            self.update_display()
            self.update_navigation()

    def next_card(self):
        """Go to the next card."""
        if self.current_index < len(self.flashcards) - 1:
            self.current_index += 1
            self.showing_front = True
            self.update_display()
            self.update_navigation()

    def update_fonts(self, window_width=1400, window_height=900):
        """Update font sizes based on window dimensions."""
        font_size = AppStyles.calculate_font_size(
            self.base_font_size, 1400, 900, window_width, window_height
        )

        # Update button fonts and sizes
        button_font = QFont("Segoe UI", font_size)
        button_height = max(35, font_size * 3)
        button_width = max(100, font_size * 10)

        for button in [self.prev_button, self.flip_button, self.next_button]:
            button.setFont(button_font)
            button.setFixedHeight(button_height)
            button.setFixedWidth(button_width)

        # Update label fonts
        title_font = QFont("Segoe UI", font_size + 2, QFont.Bold)
        content_font = QFont("Segoe UI", font_size + 1)
        small_font = QFont("Segoe UI", max(9, font_size - 2))

        if hasattr(self, "title_label"):
            self.title_label.setFont(title_font)
        if hasattr(self, "content_label"):
            self.content_label.setFont(content_font)
        if hasattr(self, "counter_label"):
            self.counter_label.setFont(small_font)
        if hasattr(self, "side_label"):
            self.side_label.setFont(QFont("Segoe UI", font_size, QFont.Bold))
        if hasattr(self, "flip_hint"):
            self.flip_hint.setFont(small_font)
