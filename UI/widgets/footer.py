"""
Footer widget for StudyGenius application.
Displays version information and credits.
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class FooterWidget(QWidget):
    """Widget for displaying footer information."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 5)

        # Create footer frame
        footer_frame = QFrame()
        footer_frame.setFrameStyle(QFrame.HLine)
        footer_frame.setStyleSheet(
            """
            QFrame {
                color: #dee2e6;
                background-color: transparent;
            }
        """
        )

        # Footer layout
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 5, 0, 0)

        # Version info
        version_label = QLabel("StudyGenius v1.0.0")
        version_label.setFont(QFont("Segoe UI", 9))
        version_label.setStyleSheet("color: #6c757d;")
        footer_layout.addWidget(version_label)

        footer_layout.addStretch()

        # Credits
        credits_label = QLabel("Developed with ❤️ for students")
        credits_label.setFont(QFont("Segoe UI", 9))
        credits_label.setStyleSheet("color: #6c757d;")
        footer_layout.addWidget(credits_label)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(footer_frame)

        footer_widget = QWidget()
        footer_widget.setLayout(footer_layout)
        main_layout.addWidget(footer_widget)

        layout.addLayout(main_layout)
