import os
from pathlib import Path
import PyPDF2
from typing import Union, Optional


class TextTransformer:
    """
    A class to extract text from PDF and TXT files.
    Only accepts .pdf and .txt file formats.
    """

    SUPPORTED_FORMATS = {".pdf", ".txt"}

    def __init__(self):
        pass

    def is_supported_format(self, file_path: Union[str, Path]) -> bool:
        """
        Check if the file format is supported (.pdf or .txt).

        Args:
            file_path: Path to the file

        Returns:
            bool: True if format is supported, False otherwise
        """
        file_extension = Path(file_path).suffix.lower()
        return file_extension in self.SUPPORTED_FORMATS

    def extract_text_from_pdf(self, file_path: Union[str, Path]) -> str:
        """
        Extract text from a PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            str: Extracted text from the PDF

        Raises:
            Exception: If there's an error reading the PDF
        """
        try:
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""

                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"

                return text.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")

    def extract_text_from_txt(self, file_path: Union[str, Path]) -> str:
        """
        Extract text from a TXT file.

        Args:
            file_path: Path to the TXT file

        Returns:
            str: Content of the TXT file

        Raises:
            Exception: If there's an error reading the TXT file
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding if utf-8 fails
            try:
                with open(file_path, "r", encoding="latin-1") as file:
                    return file.read()
            except Exception as e:
                raise Exception(
                    f"Error reading TXT file with multiple encodings: {str(e)}"
                )
        except Exception as e:
            raise Exception(f"Error reading TXT file: {str(e)}")

    def transform_file(self, file_path: Union[str, Path]) -> Optional[str]:
        """
        Extract text from a file (PDF or TXT).

        Args:
            file_path: Path to the file

        Returns:
            str: Extracted text from the file
            None: If file format is not supported

        Raises:
            FileNotFoundError: If the file doesn't exist
            Exception: If there's an error processing the file
        """
        file_path = Path(file_path)

        # Check if file exists
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check if format is supported
        if not self.is_supported_format(file_path):
            print(
                f"Unsupported file format. Only {', '.join(self.SUPPORTED_FORMATS)} files are accepted."
            )
            return None

        file_extension = file_path.suffix.lower()

        if file_extension == ".pdf":
            return self.extract_text_from_pdf(file_path)
        elif file_extension == ".txt":
            return self.extract_text_from_txt(file_path)

    def process_file(
        self, file_path: Union[str, Path], output_to_console: bool = True
    ) -> Optional[str]:
        try:
            extracted_text = self.transform_file(file_path)

            if extracted_text is not None:
                if output_to_console:
                    print(f"\n--- Text extracted from {Path(file_path).name} ---")
                    print(extracted_text)
                    print(f"\n--- End of {Path(file_path).name} ---\n")

                return extracted_text

            return None

        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return None


def main():
    """
    Main function to demonstrate usage of TextTransformer.
    """
    transformer = TextTransformer()

    # Example usage
    print("TextTransformer - Extract text from PDF and TXT files")
    print("Supported formats: .pdf, .txt")

    # You can uncomment and modify these lines to test with actual files
    # file_path = input("Enter the path to your file: ")
    # transformer.process_file(file_path)


if __name__ == "__main__":
    main()
