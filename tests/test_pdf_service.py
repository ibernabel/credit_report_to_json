import os
import pytest
from pathlib import Path
from app.services.pdf_service import PDFService

class TestPDFService:
    @pytest.fixture
    def pdf_service(self, test_output_dir):
        # Use test directories
        test_pdf_dir = os.path.join("tests", "test_files")
        return PDFService(credit_reports_dir=test_pdf_dir, output_dir=test_output_dir)

    def test_init_creates_directories(self, test_output_dir):
        # Test that directories are created on initialization
        test_pdf_dir = os.path.join("tests", "test_init_pdf_dir")
        test_out_dir = os.path.join("tests", "test_init_out_dir")
        
        service = PDFService(credit_reports_dir=test_pdf_dir, output_dir=test_out_dir)
        
        assert Path(test_pdf_dir).exists()
        assert Path(test_out_dir).exists()
        
        # Cleanup
        os.rmdir(test_pdf_dir)
        os.rmdir(test_out_dir)

    def test_convert_pdf_to_text_with_save(self, pdf_service, test_pdf_path, test_output_dir):
        # For testing purposes, we'll use a text file
        filename = "test_credit_report.txt"
        source_path = os.path.join("tests", "test_files", filename)
        target_path = os.path.join(pdf_service.credit_reports_dir, filename)
        
        # Copy test file to credit_reports directory
        import shutil
        shutil.copy2(source_path, target_path)
        
        # Test text file processing
        pdf_service.convert_pdf_to_text(filename, save_output=True)
        
        expected_output = os.path.join(test_output_dir, filename)
        assert os.path.exists(expected_output)
        
        # Verify content
        with open(expected_output, 'r', encoding='utf-8') as f:
            content = f.read()
        assert content.strip() != ""
        assert "suscriptor" in content.lower()  # Basic content verification

    def test_convert_pdf_to_text_without_save(self, pdf_service, test_pdf_path):
        # For testing purposes, we'll use a text file
        filename = "test_credit_report.txt"
        source_path = os.path.join("tests", "test_files", filename)
        target_path = os.path.join(pdf_service.credit_reports_dir, filename)
        
        # Copy test file to credit_reports directory
        import shutil
        shutil.copy2(source_path, target_path)
        
        # Test text file processing
        result = pdf_service.convert_pdf_to_text(filename, save_output=False)
        
        assert result is not None
        assert isinstance(result, str)
        assert result.strip() != ""
        assert "suscriptor" in result.lower()  # Basic content verification

    def test_cleanup_temp_files(self, pdf_service, test_output_dir):
        # First create some files
        filename = "test_credit_report.txt"
        base_name = filename.replace('.txt', '')
        
        # Create test files
        source_path = os.path.join("tests", "test_files", filename)
        target_path = os.path.join(pdf_service.credit_reports_dir, filename)
        txt_path = os.path.join(test_output_dir, filename)
        
        # Copy test file and create output file
        import shutil
        shutil.copy2(source_path, target_path)
        Path(txt_path).touch()
        
        # Test cleanup
        pdf_service.cleanup_temp_files(base_name)
        
        assert not os.path.exists(target_path)
        assert not os.path.exists(txt_path)

    def test_file_not_found_error(self, pdf_service):
        with pytest.raises(FileNotFoundError):
            pdf_service.convert_pdf_to_text("nonexistent.txt")

    def test_invalid_file_error(self, pdf_service, test_output_dir):
        # Create an invalid file
        invalid_file = os.path.join(pdf_service.credit_reports_dir, "invalid.txt")
        with open(invalid_file, 'w') as f:
            f.write("")  # Empty file
        
        with pytest.raises(Exception) as exc_info:
            pdf_service.convert_pdf_to_text("invalid.txt")
        
        assert "Error processing file" in str(exc_info.value)
        
        # Cleanup
        os.remove(invalid_file)
