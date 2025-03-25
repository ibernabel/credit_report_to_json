"""PDF Service for handling PDF to text conversion operations."""
import fitz  # PyMuPDF
import unidecode
import os
from pathlib import Path
from typing import Optional


class PDFService:
    """Service for handling PDF to text conversion operations."""

    def __init__(self, credit_reports_dir: str = './credit_reports', output_dir: str = './output_text'):
        """Initialize the PDF service with configurable directories.

        Args:
            credit_reports_dir (str): Directory for PDF files
            output_dir (str): Directory for output text files
        """
        self.credit_reports_dir = Path(credit_reports_dir)
        self.output_dir = Path(output_dir)
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Ensure required directories exist."""
        self.credit_reports_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)

    def convert_pdf_to_text(self, filename: str, save_output: bool = True) -> Optional[str]:
        """Convert PDF file to text.

        Args:
            filename (str): Name of the file (with or without extension)
            save_output (bool): Whether to save the output to a text file

        Returns:
            str: Extracted and processed text if save_output is False,
                 None if save_output is True (file is saved instead)

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is not valid
            Exception: For other processing errors
        """
        try:
            # For testing purposes, handle both PDF and text files
            if not (filename.lower().endswith('.pdf') or filename.lower().endswith('.txt')):
                filename = f"{filename}.txt" if os.path.exists(self.credit_reports_dir / f"{filename}.txt") else f"{filename}.pdf"

            file_path = self.credit_reports_dir / filename
            
            if not file_path.exists():
                raise FileNotFoundError(f"No file found at: {file_path}")

            # Process file based on type
            if filename.lower().endswith('.pdf'):
                # Open and process PDF
                doc = fitz.open(str(file_path))
                text = ''
                for page in doc:
                    text += page.get_text()
                doc.close()
            else:
                # Read text file directly
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            
            # Process text
            processed_text = unidecode.unidecode(text.lower())

            if save_output:
                # Generate output filename
                output_filename = file_path.stem + '.txt'
                output_path = self.output_dir / output_filename
                
                # Save to file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(processed_text)
                return None
            
            return processed_text

        except fitz.fitz.FileNotFoundError:
            raise FileNotFoundError(f"Could not open file: {filename}")
        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")

    def cleanup_temp_files(self, filename: str) -> None:
        """Clean up temporary files after processing.

        Args:
            filename (str): Name of the file to clean up (without extension)
        """
        try:
            # Remove text output file if it exists
            text_file = self.output_dir / f"{filename}.txt"
            if text_file.exists():
                text_file.unlink()

            # Remove PDF file if it exists
            pdf_file = self.credit_reports_dir / f"{filename}.pdf"
            if pdf_file.exists():
                pdf_file.unlink()

        except Exception as e:
            raise Exception(f"Error cleaning up temporary files: {str(e)}")
