import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

class TestAPI:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_upload_invalid_file(self, client):
        # Test uploading an invalid file type
        files = {
            "file": ("test.jpg", "test content", "image/jpeg")
        }
        response = client.post("/api/v1/credit-report", files=files)
        
        assert response.status_code == 400
        assert "Invalid file format" in response.json()["detail"]

    def test_upload_valid_file(self, client):
        # Test uploading a valid text file
        test_file_path = os.path.join("tests", "test_files", "test_credit_report.txt")
        if not os.path.exists(test_file_path):
            pytest.skip(f"Test file not found at {test_file_path}")
            
        with open(test_file_path, "rb") as file:
            files = {
                "file": ("test_credit_report.txt", file, "text/plain")
            }
            response = client.post("/api/v1/credit-report", files=files)
            
            assert response.status_code == 200
            assert "message" in response.json()

    def test_upload_credit_report(self, client):
        # Test uploading a valid credit report PDF file
        test_file_path = "./credit-report.pdf"
        if not os.path.exists(test_file_path):
            pytest.skip(f"Test file not found at {test_file_path}")
            
        with open(test_file_path, "rb") as file:
            files = {
                "file": ("credit-report.pdf", file, "application/pdf")
            }
            response = client.post("/api/v1/credit-report", files=files)
            
            assert response.status_code == 200
            assert "message" in response.json()
        # Test request without file
        response = client.post("/api/v1/credit-report")
        assert response.status_code == 422  # Unprocessable Entity

    def test_upload_empty_file(self, client):
        # Test uploading an empty file
        files = {
            "file": ("empty.pdf", b"", "application/pdf")
        }
        response = client.post("/api/v1/credit-report", files=files)
        
        assert response.status_code == 400
        assert "error" in response.json()["detail"].lower()

    def test_large_file_upload(self, client):
        # Test uploading a large file
        large_content = b"0" * (10 * 1024 * 1024)  # 10MB file
        files = {
            "file": ("large.txt", large_content, "text/plain")
        }
        response = client.post("/api/v1/credit-report", files=files)
        
        # Either expect a 413 Payload Too Large or successful processing
        assert response.status_code in [413, 200]

    def test_concurrent_uploads(self, client):
        # Test concurrent uploads
        test_file_path = os.path.join("tests", "test_files", "test_credit_report.txt")
        if not os.path.exists(test_file_path):
            pytest.skip(f"Test file not found at {test_file_path}")
            
        import concurrent.futures
        
        def upload_file():
            with open(test_file_path, "rb") as file:
                files = {
                    "file": ("test_credit_report.txt", file, "text/plain")
                }
                return client.post("/api/v1/credit-report", files=files)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(upload_file) for _ in range(3)]
            responses = [future.result() for future in futures]
            
        # Check all responses were successful
        assert all(response.status_code == 200 for response in responses)
