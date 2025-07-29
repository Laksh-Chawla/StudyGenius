"""
Application styles for StudyGenius.
Contains centralized styling definitions for responsive UI appearance.
"""


class AppStyles:
    """Centralized styling for the StudyGenius application with responsive design."""

    @staticmethod
    def get_main_window_style():
        """Get the main window stylesheet."""
        return """
            QMainWindow {
                background-color: #f5f5f5;
                color: #333;
            }
            QMainWindow::separator {
                background-color: #dee2e6;
                width: 1px;
                height: 1px;
            }
            QStatusBar {
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
                color: #6c757d;
            }
            QSplitter::handle {
                background-color: #dee2e6;
                width: 2px;
            }
            QSplitter::handle:hover {
                background-color: #0078d4;
            }
        """

    @staticmethod
    def get_title_style():
        """Get the title label stylesheet."""
        return """
            QLabel {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #0078d4, stop: 1 #106ebe);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
        """

    @staticmethod
    def get_widget_frame_style():
        """Get the standard widget frame stylesheet."""
        return """
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 15px;
            }
        """

    @staticmethod
    def get_button_primary_style():
        """Get the primary button stylesheet."""
        return """
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 100px;
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

    @staticmethod
    def get_button_secondary_style():
        """Get the secondary button stylesheet."""
        return """
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 100px;
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

    @staticmethod
    def get_text_edit_style():
        """Get the text edit stylesheet."""
        return """
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 12px;
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.4;
                selection-background-color: #0078d4;
                selection-color: white;
            }
            QTextEdit:focus {
                border-color: #0078d4;
                outline: none;
                box-shadow: 0 0 0 0.2rem rgba(0, 120, 212, 0.25);
            }
        """

    @staticmethod
    def get_group_box_style():
        """Get the group box stylesheet."""
        return """
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: #495057;
                background-color: transparent;
            }
        """

    @staticmethod
    def calculate_font_size(
        base_size,
        window_width=1400,
        window_height=900,
        current_width=1400,
        current_height=900,
    ):
        """Calculate responsive font size based on window dimensions."""
        scale_factor = min(current_width / window_width, current_height / window_height)
        scale_factor = max(1.2, min(scale_factor, 2.5))  # Much larger: 1.2 to 2.5
        return max(12, int(base_size * scale_factor))  # Minimum font size of 12

    @staticmethod
    def get_responsive_button_style(font_size=14):
        """Get responsive button stylesheet."""
        return f"""
            QPushButton {{
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: {max(12, font_size)}px {max(20, font_size+8)}px;
                font-weight: bold;
                font-size: {font_size}px;
                min-width: {max(120, font_size*10)}px;
            }}
            QPushButton:hover {{
                background-color: #106ebe;
            }}
            QPushButton:pressed {{
                background-color: #005a9e;
            }}
            QPushButton:disabled {{
                background-color: #e9ecef;
                color: #6c757d;
            }}
        """

    @staticmethod
    def get_responsive_text_style(font_size=14):
        """Get responsive text edit stylesheet."""
        return f"""
            QTextEdit {{
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: {max(12, font_size)}px;
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: {font_size}px;
                line-height: 1.4;
                selection-background-color: #0078d4;
                selection-color: white;
            }}
            QTextEdit:focus {{
                border-color: #0078d4;
                outline: none;
            }}
        """

    @staticmethod
    def get_responsive_label_style(font_size=14, color="#333"):
        """Get responsive label stylesheet."""
        return f"""
            QLabel {{
                color: {color};
                font-size: {font_size}px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """
