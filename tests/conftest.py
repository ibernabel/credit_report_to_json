import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def test_pdf_path():
    # This fixture should point to a test PDF file that will be used for testing
    return os.path.join("tests", "test_files", "test_credit_report.pdf")

@pytest.fixture
def test_output_dir():
    # Create a temporary directory for test outputs
    test_dir = os.path.join("tests", "test_output")
    os.makedirs(test_dir, exist_ok=True)
    yield test_dir
    # Clean up test files after tests
    for file in os.listdir(test_dir):
        os.remove(os.path.join(test_dir, file))
    os.rmdir(test_dir)

@pytest.fixture
def sample_text_content():
    return """
    EQUIFAX
    CREDIT REPORT

    Personal Information:
    Name: JOHN DOE
    SSN: XXX-XX-1234
    Date of Birth: 01/01/1980

    Credit Score: 750

    Account Summary:
    Open Accounts: 5
    Closed Accounts: 2
    """
