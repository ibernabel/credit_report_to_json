from pydantic import BaseModel
from typing import List, Optional

class PersonalInfo(BaseModel):
    """Personal information from the credit report."""
    name: Optional[str] = None
    identification: Optional[str] = None
    address: Optional[str] = None

class CreditAccount(BaseModel):
    """Individual credit account information."""
    institution: str
    account_type: str
    account_number: str
    status: str
    balance: float
    payment_history: Optional[List[str]] = None

class CreditReport(BaseModel):
    """Complete credit report data structure."""
    personal_info: PersonalInfo
    accounts: List[CreditAccount]
    report_date: str
    score: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "personal_info": {
                    "name": "John Doe",
                    "identification": "001-0123456-7",
                    "address": "123 Main St, City"
                },
                "accounts": [
                    {
                        "institution": "Bank Name",
                        "account_type": "Credit Card",
                        "account_number": "****1234",
                        "status": "Active",
                        "balance": 1500.00,
                        "payment_history": ["Current", "Current", "Current"]
                    }
                ],
                "report_date": "2024-03-25",
                "score": 750
            }
        }
