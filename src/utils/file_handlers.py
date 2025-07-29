"""
File handlers for StudyGenius application.
Handles reading and processing of different file types.
"""

import os
from typing import Optional


class PDFHandler:
    """Handler for PDF file operations."""

    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract text from a PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            Extracted text content

        Raises:
            Exception: If PDF processing fails
        """
        try:
            # Try importing PyPDF2 first
            try:
                import PyPDF2

                return PDFHandler._extract_with_pypdf2(file_path)
            except ImportError:
                pass

            # Try importing pdfplumber as alternative
            try:
                import pdfplumber

                return PDFHandler._extract_with_pdfplumber(file_path)
            except ImportError:
                pass

            # If no PDF libraries available, raise error
            raise Exception(
                "No PDF processing library found. Please install PyPDF2 or pdfplumber:\n"
                "pip install PyPDF2\n"
                "or\n"
                "pip install pdfplumber"
            )

        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")

    @staticmethod
    def _extract_with_pypdf2(file_path: str) -> str:
        """Extract text using PyPDF2."""
        import PyPDF2

        text = ""
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"

        return text.strip()

    @staticmethod
    def _extract_with_pdfplumber(file_path: str) -> str:
        """Extract text using pdfplumber."""
        import pdfplumber

        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return text.strip()


class TextHandler:
    """Handler for text file operations."""

    @staticmethod
    def read_text(file_path: str) -> str:
        """
        Read text from a text file.

        Args:
            file_path: Path to the text file

        Returns:
            File content as string

        Raises:
            Exception: If file reading fails
        """
        try:
            # Try different encodings
            encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]

            for encoding in encodings:
                try:
                    with open(file_path, "r", encoding=encoding) as file:
                        content = file.read()
                        return content.strip()
                except UnicodeDecodeError:
                    continue

            # If all encodings fail, try binary mode and decode with errors='replace'
            with open(file_path, "rb") as file:
                content = file.read()
                return content.decode("utf-8", errors="replace").strip()

        except Exception as e:
            raise Exception(f"Failed to read text file: {str(e)}")

    @staticmethod
    def write_text(file_path: str, content: str, encoding: str = "utf-8") -> None:
        """
        Write text to a file.

        Args:
            file_path: Path to the output file
            content: Text content to write
            encoding: Text encoding (default: utf-8)

        Raises:
            Exception: If file writing fails
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "w", encoding=encoding) as file:
                file.write(content)

        except Exception as e:
            raise Exception(f"Failed to write text file: {str(e)}")


class DocumentProcessor:
    """General document processing utilities."""

    @staticmethod
    def get_supported_extensions() -> list:
        """Get list of supported file extensions."""
        return [".txt", ".pdf"]

    @staticmethod
    def is_supported_file(file_path: str) -> bool:
        """Check if file type is supported."""
        ext = os.path.splitext(file_path)[1].lower()
        return ext in DocumentProcessor.get_supported_extensions()

    @staticmethod
    def extract_text_from_file(file_path: str) -> str:
        """
        Extract text from any supported file type.

        Args:
            file_path: Path to the file

        Returns:
            Extracted text content

        Raises:
            Exception: If file type is unsupported or processing fails
        """
        if not os.path.exists(file_path):
            raise Exception(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            return PDFHandler.extract_text(file_path)
        elif ext == ".txt":
            return TextHandler.read_text(file_path)
        else:
            raise Exception(f"Unsupported file type: {ext}")

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text content.

        Args:
            text: Raw text content

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Remove excessive whitespace
        lines = text.split("\n")
        cleaned_lines = []

        for line in lines:
            line = line.strip()
            if line:  # Skip empty lines
                cleaned_lines.append(line)

        # Join lines with single spaces, but preserve paragraph breaks
        result = []
        current_paragraph = []

        for line in cleaned_lines:
            if line.endswith(".") or line.endswith("!") or line.endswith("?"):
                current_paragraph.append(line)
                result.append(" ".join(current_paragraph))
                current_paragraph = []
            else:
                current_paragraph.append(line)

        # Add any remaining text
        if current_paragraph:
            result.append(" ".join(current_paragraph))

        return "\n\n".join(result)
