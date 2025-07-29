#!/usr/bin/env python3
"""
StudyGenius UI Main - Clean UI Components Launcher
A modern Windows desktop UI for StudyGenius with responsive font sizing.
"""

import sys
import os

# Add src directory to Python path for imports
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QSplitter,
    QDesktopWidget,
    QTextEdit,
    QScrollArea,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
from UI.widgets.file_upload import FileUploadWidget
from UI.widgets.text_display import TextDisplayWidget
from UI.widgets.action_buttons import ActionButtonsWidget
from UI.widgets.flashcards import FlashcardsWidget
from UI.widgets.quiz import QuizWidget
from UI.widgets.insights import InsightsWidget
from UI.widgets.footer import FooterWidget
from src.utils.styles import AppStyles

# Import summarizer
from src.summarizer import TextSummarizer


class StudyGeniusUI(QMainWindow):
    """Main UI window for StudyGenius with responsive design."""

    # Signals for backend integration
    file_uploaded = pyqtSignal(str, str)  # file_path, content
    summarize_requested = pyqtSignal(str)  # text
    flashcards_requested = pyqtSignal(str)  # text
    quiz_requested = pyqtSignal(str)  # text

    def __init__(self):
        super().__init__()
        self.base_font_size = 14  # Increased from 11 to 14

        # Initialize summarizer
        self.summarizer = TextSummarizer()

        self.init_ui()
        self.setup_connections()
        self.setup_responsive_fonts()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("StudyGenius – AI Text Analyzer")
        self.setMinimumSize(1200, 800)

        # Center window on screen
        self.center_window()

        # Apply application styles
        self.setStyleSheet(AppStyles.get_main_window_style())

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Create left panel (main content)
        left_panel = self.create_left_panel()

        # Create right panel (insights)
        right_panel = self.create_right_panel()

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([900, 300])  # Initial sizes

        main_layout.addWidget(splitter)

        # Status bar
        self.statusBar().showMessage("Ready")

    def center_window(self):
        """Center the window on the screen."""
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2
        )

    def create_left_panel(self):
        """Create the left panel with main functionality."""
        # Create a scroll area for the entire left panel
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Create the actual content widget
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(15)
        left_layout.setContentsMargins(5, 5, 5, 5)

        # Title section
        self.title_label = QLabel("StudyGenius – AI Text Analyzer")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(AppStyles.get_title_style())
        left_layout.addWidget(self.title_label)

        # File upload section
        self.file_upload_widget = FileUploadWidget()
        left_layout.addWidget(self.file_upload_widget)

        # Text display section
        self.text_display_widget = TextDisplayWidget()
        left_layout.addWidget(self.text_display_widget)

        # Action buttons section
        self.action_buttons_widget = ActionButtonsWidget()
        left_layout.addWidget(self.action_buttons_widget)

        # Content display section (flashcards/quiz/summary)
        self.content_stack = QStackedWidget()

        # Default view
        self.default_view = QLabel(
            "Upload a file and generate content to see flashcards or quiz questions here."
        )
        self.default_view.setAlignment(Qt.AlignCenter)
        self.default_view.setStyleSheet("color: #666; padding: 50px;")
        self.content_stack.addWidget(self.default_view)

        # Summary view
        self.summary_widget = self.create_summary_widget()
        self.content_stack.addWidget(self.summary_widget)

        # Flashcards view
        self.flashcards_widget = FlashcardsWidget()
        self.content_stack.addWidget(self.flashcards_widget)

        # Quiz view
        self.quiz_widget = QuizWidget()
        self.content_stack.addWidget(self.quiz_widget)

        left_layout.addWidget(self.content_stack)

        # Footer
        self.footer_widget = FooterWidget()
        left_layout.addWidget(self.footer_widget)

        # Set the content widget in the scroll area
        scroll_area.setWidget(left_widget)

        return scroll_area

    def create_right_panel(self):
        """Create the right panel with insights."""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 0, 5, 0)

        # Insights widget
        self.insights_widget = InsightsWidget()
        right_layout.addWidget(self.insights_widget)

        # Stretch to fill remaining space
        right_layout.addStretch()

        return right_widget

    def create_summary_widget(self):
        """Create the summary display widget."""
        summary_widget = QWidget()
        layout = QVBoxLayout(summary_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title_label = QLabel("📄 Text Summary")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Summary info
        self.summary_info_label = QLabel()
        self.summary_info_label.setFont(QFont("Segoe UI", 11))
        self.summary_info_label.setStyleSheet("color: #7f8c8d; margin-bottom: 5px;")
        self.summary_info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.summary_info_label)

        # Summary text area - no scroll area, just a simple text edit
        self.summary_text_area = QTextEdit()
        self.summary_text_area.setReadOnly(True)
        self.summary_text_area.setFont(QFont("Segoe UI", 13))
        # Remove height constraints to let it expand naturally
        self.summary_text_area.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.summary_text_area.setStyleSheet(
            """
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                padding: 12px;
                background-color: #ffffff;
                color: #2c3e50;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QTextEdit:focus {
                border-color: #3498db;
            }
        """
        )
        self.summary_text_area.setPlaceholderText("Summary will appear here...")
        self.summary_text_area.setLineWrapMode(QTextEdit.WidgetWidth)
        self.summary_text_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.summary_text_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout.addWidget(self.summary_text_area)

        # Summary statistics
        self.summary_stats_label = QLabel()
        self.summary_stats_label.setFont(QFont("Segoe UI", 10))
        self.summary_stats_label.setStyleSheet(
            """
            QLabel {
                color: #7f8c8d; 
                padding: 8px;
                background-color: #ecf0f1;
                border-radius: 4px;
                margin-top: 5px;
            }
        """
        )
        self.summary_stats_label.setAlignment(Qt.AlignCenter)
        self.summary_stats_label.setWordWrap(True)
        layout.addWidget(self.summary_stats_label)

        return summary_widget

    def setup_connections(self):
        """Setup signal-slot connections between widgets."""
        # File upload connections
        self.file_upload_widget.file_uploaded.connect(self.handle_file_upload)

        # Action button connections
        self.action_buttons_widget.summarize_clicked.connect(self.handle_summarize)
        self.action_buttons_widget.flashcards_clicked.connect(self.handle_flashcards)
        self.action_buttons_widget.quiz_clicked.connect(self.handle_quiz)

        # Text display connections
        self.text_display_widget.text_changed.connect(self.handle_text_change)

    def setup_responsive_fonts(self):
        """Setup responsive font sizing based on window size."""
        # Calculate font size based on window dimensions
        width = self.width()
        height = self.height()

        # Base calculation: scale font with window size
        scale_factor = min(width / 1400, height / 900)  # Based on default window size
        scale_factor = max(1.2, min(scale_factor, 2.5))  # Much larger scaling

        font_size = int(self.base_font_size * scale_factor)
        title_size = int(28 * scale_factor)  # Increased title size

        # Update title font
        title_font = QFont("Segoe UI", title_size, QFont.Bold)
        self.title_label.setFont(title_font)

        # Update default view font
        default_font = QFont("Segoe UI", font_size)
        self.default_view.setFont(default_font)

        # Update summary widget fonts
        if hasattr(self, "summary_text_area"):
            summary_title_font = QFont("Segoe UI", int(16 * scale_factor), QFont.Bold)
            summary_text_font = QFont("Segoe UI", int(13 * scale_factor))
            summary_info_font = QFont("Segoe UI", int(11 * scale_factor))
            summary_stats_font = QFont("Segoe UI", int(10 * scale_factor))

            # Find the title label in summary widget
            for child in self.summary_widget.findChildren(QLabel):
                if "Text Summary" in child.text():
                    child.setFont(summary_title_font)
                    break

            self.summary_text_area.setFont(summary_text_font)
            self.summary_info_label.setFont(summary_info_font)
            self.summary_stats_label.setFont(summary_stats_font)

        # Update all widgets with responsive fonts
        self.text_display_widget.update_fonts(width, height)
        self.action_buttons_widget.update_fonts(width, height)
        self.flashcards_widget.update_fonts(width, height)
        self.quiz_widget.update_fonts(width, height)
        self.insights_widget.update_fonts(width, height)

    def resizeEvent(self, event):
        """Handle window resize events for responsive font sizing."""
        super().resizeEvent(event)
        # Delay font update slightly to avoid excessive calls during resize
        QTimer.singleShot(100, self.setup_responsive_fonts)

    # Backend Integration Methods (for connecting to your main.py later)

    def handle_file_upload(self, file_path, content):
        """Handle file upload and emit signal for backend processing."""
        self.text_display_widget.set_text(content)
        self.insights_widget.update_file_info(file_path, len(content))
        self.statusBar().showMessage(f"File loaded: {os.path.basename(file_path)}")

        # Emit signal for backend
        self.file_uploaded.emit(file_path, content)

    def handle_text_change(self, text):
        """Handle text changes in the display widget."""
        word_count = len(text.split()) if text.strip() else 0
        self.insights_widget.update_text_stats(word_count, text)

    def handle_summarize(self):
        """Handle summarize button click - perform text summarization."""
        text = self.text_display_widget.get_text()
        if not text.strip():
            self.statusBar().showMessage("No text to summarize")
            return

        self.statusBar().showMessage("Processing summarization...")

        try:
            # Perform summarization
            result = self.summarizer.summarize_auto(text)

            if result["success"]:
                # Display the summary
                self.summary_text_area.setPlainText(result["summary"])
                self.adjust_summary_text_height()

                # Update info label
                self.summary_info_label.setText(
                    f"Generated using {result['algorithm']} algorithm"
                )

                # Get and display statistics
                stats = self.summarizer.get_summary_stats(text, result["summary"])
                if stats:
                    stats_text = (
                        f"Original: {stats['original_words']} words • "
                        f"Summary: {stats['summary_words']} words • "
                        f"Compression: {stats['reduction_percentage']}% reduction"
                    )
                    self.summary_stats_label.setText(stats_text)

                # Switch to summary view
                self.content_stack.setCurrentWidget(self.summary_widget)

                # Update status
                self.statusBar().showMessage("Summary generated successfully")

                # Also emit the signal for any external listeners
                self.summarize_requested.emit(text)

            else:
                # Handle summarization failure
                self.summary_text_area.setPlainText(
                    "Failed to generate summary. Please try again."
                )
                self.adjust_summary_text_height()
                self.summary_info_label.setText("Summarization failed")
                self.summary_stats_label.setText("")
                self.content_stack.setCurrentWidget(self.summary_widget)
                self.statusBar().showMessage("Summarization failed")

        except Exception as e:
            # Handle any unexpected errors
            error_msg = f"Error during summarization: {str(e)}"
            self.summary_text_area.setPlainText(error_msg)
            self.summary_info_label.setText("Error occurred")
            self.summary_stats_label.setText("")
            self.content_stack.setCurrentWidget(self.summary_widget)
            self.statusBar().showMessage("Summarization error")

    def handle_flashcards(self):
        """Handle flashcards button click - emit signal for backend."""
        text = self.text_display_widget.get_text()
        if not text.strip():
            self.statusBar().showMessage("No text to generate flashcards from")
            return

        self.statusBar().showMessage("Generating flashcards...")
        self.flashcards_requested.emit(text)

    def handle_quiz(self):
        """Handle quiz button click - emit signal for backend."""
        text = self.text_display_widget.get_text()
        if not text.strip():
            self.statusBar().showMessage("No text to generate quiz from")
            return

        self.statusBar().showMessage("Creating quiz...")
        self.quiz_requested.emit(text)

    # Methods for backend to call (your main.py can call these)

    def display_summary(self, summary_text):
        """Display summary result from backend."""
        # You can implement this to show summary in a dialog or text widget
        self.statusBar().showMessage("Summary generated")

    def display_flashcards(self, flashcards_data):
        """Display flashcards from backend processing."""
        if flashcards_data:
            self.flashcards_widget.set_flashcards(flashcards_data)
            self.content_stack.setCurrentWidget(self.flashcards_widget)
            self.statusBar().showMessage(f"{len(flashcards_data)} flashcards generated")
        else:
            self.statusBar().showMessage("No flashcards could be generated")

    def display_quiz(self, quiz_data):
        """Display quiz from backend processing."""
        if quiz_data:
            self.quiz_widget.set_questions(quiz_data)
            self.content_stack.setCurrentWidget(self.quiz_widget)
            self.statusBar().showMessage(f"{len(quiz_data)} quiz questions generated")
        else:
            self.statusBar().showMessage("No quiz questions could be generated")

    def get_current_text(self):
        """Get current text content (for backend access)."""
        return self.text_display_widget.get_text()

    def set_status_message(self, message):
        """Set status bar message (for backend feedback)."""
        self.statusBar().showMessage(message)

    def adjust_summary_text_height(self):
        """Adjust the height of the summary text area based on content."""
        if hasattr(self, "summary_text_area"):
            # Get the document and calculate required height
            doc = self.summary_text_area.document()
            doc.setTextWidth(self.summary_text_area.viewport().width())
            height = doc.size().height()

            # Set minimum and maximum heights
            min_height = 100
            max_height = 600

            # Calculate the final height
            final_height = max(min_height, min(max_height, int(height) + 20))

            # Set the height
            self.summary_text_area.setFixedHeight(final_height)


def run_ui():
    """Launch the StudyGenius UI."""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("StudyGenius")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("StudyGenius")

    # Apply Windows-native styling
    app.setStyle("Fusion")

    # Create and show main window
    window = StudyGeniusUI()
    window.show()

    return app, window


if __name__ == "__main__":
    app, window = run_ui()
    sys.exit(app.exec_())
