"""
File upload widget for StudyGenius application.
Handles PDF and TXT file uploads with drag-and-drop support.
"""

import os
import sys

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
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QFont
from src.utils.file_handlers import PDFHandler, TextHandler


class FileUploadWidget(QWidget):
    """Widget for handling file uploads with drag-and-drop support."""

    file_uploaded = pyqtSignal(str, str)  # file_path, content

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_drag_drop()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Create upload frame
        self.upload_frame = QFrame()
        self.upload_frame.setFrameStyle(QFrame.StyledPanel)
        self.upload_frame.setStyleSheet(
            """
            QFrame {
                border: 2px dashed #ccc;
                border-radius: 8px;
                background-color: #f9f9f9;
                padding: 20px;
            }
            QFrame:hover {
                border-color: #0078d4;
                background-color: #f0f8ff;
            }
        """
        )

        frame_layout = QVBoxLayout(self.upload_frame)
        frame_layout.setAlignment(Qt.AlignCenter)

        # Upload icon/text
        upload_label = QLabel("📁 Drop files here or click to browse")
        upload_label.setAlignment(Qt.AlignCenter)
        upload_label.setFont(QFont("Segoe UI", 12))
        upload_label.setStyleSheet(
            "color: #666; border: none; background: transparent;"
        )
        frame_layout.addWidget(upload_label)

        # Supported formats label
        formats_label = QLabel("Supported formats: PDF, TXT")
        formats_label.setAlignment(Qt.AlignCenter)
        formats_label.setFont(QFont("Segoe UI", 10))
        formats_label.setStyleSheet(
            "color: #999; border: none; background: transparent;"
        )
        frame_layout.addWidget(formats_label)

        layout.addWidget(self.upload_frame)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Browse button
        self.browse_button = QPushButton("Browse Files")
        self.browse_button.setFixedHeight(35)
        self.browse_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """
        )
        self.browse_button.clicked.connect(self.browse_file)

        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedHeight(35)
        self.clear_button.setStyleSheet(
            """
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
            }
        """
        )
        self.clear_button.clicked.connect(self.clear_file)
        self.clear_button.setEnabled(False)

        buttons_layout.addWidget(self.browse_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        # File info label
        self.file_info_label = QLabel("")
        self.file_info_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(self.file_info_label)

    def setup_drag_drop(self):
        """Setup drag and drop functionality."""
        self.setAcceptDrops(True)
        self.upload_frame.mousePressEvent = self.frame_clicked

    def frame_clicked(self, event):
        """Handle frame click to open file dialog."""
        self.browse_file()

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.upload_frame.setStyleSheet(
                """
                QFrame {
                    border: 2px solid #0078d4;
                    border-radius: 8px;
                    background-color: #e6f3ff;
                    padding: 20px;
                }
            """
            )

    def dragLeaveEvent(self, event):
        """Handle drag leave event."""
        self.upload_frame.setStyleSheet(
            """
            QFrame {
                border: 2px dashed #ccc;
                border-radius: 8px;
                background-color: #f9f9f9;
                padding: 20px;
            }
            QFrame:hover {
                border-color: #0078d4;
                background-color: #f0f8ff;
            }
        """
        )

    def dropEvent(self, event: QDropEvent):
        """Handle drop event."""
        self.dragLeaveEvent(event)

        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            self.process_file(files[0])

    def browse_file(self):
        """Open file dialog to browse for files."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "Text Files (*.txt);;PDF Files (*.pdf);;All Files (*)",
        )

        if file_path:
            self.process_file(file_path)

    def process_file(self, file_path):
        """Process the selected file."""
        try:
            # Check file extension
            ext = os.path.splitext(file_path)[1].lower()

            if ext == ".pdf":
                content = PDFHandler.extract_text(file_path)
            elif ext == ".txt":
                content = TextHandler.read_text(file_path)
            else:
                QMessageBox.warning(
                    self, "Unsupported Format", "Please select a PDF or TXT file."
                )
                return

            # Update UI
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            size_mb = file_size / (1024 * 1024)

            self.file_info_label.setText(f"📄 {filename} ({size_mb:.1f} MB)")
            self.clear_button.setEnabled(True)

            # Emit signal
            self.file_uploaded.emit(file_path, content)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process file: {str(e)}")

    def clear_file(self):
        """Clear the current file."""
        self.file_info_label.setText("")
        self.clear_button.setEnabled(False)
        self.file_uploaded.emit("", "")
