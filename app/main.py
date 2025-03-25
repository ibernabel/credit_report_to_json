from fastapi import FastAPI, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
import os
from pathlib import Path
from app.services.pdf_service import PDFService
from app.services.parser_service import ParserService

app = FastAPI(
    title="Credit Report API",
    description="""
    API service for converting credit report files to structured JSON format.
    
    ## Features
    - Credit report processing (PDF and text files)
    - Structured JSON output
    - Error handling and validation
    - File cleanup after processing
    
    ## Notes
    - Accepts PDF and text files
    - Maximum file size: 10MB
    - Files are processed asynchronously
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize services
pdf_service = PDFService()
parser_service = ParserService()

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint to verify service status.
    
    Returns:
        dict: Status message indicating service health
    """
    return {"status": "healthy"}

@app.post("/api/v1/credit-report", 
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Upload and process credit report",
    description="Upload a credit report file (PDF or text) and receive structured JSON data"
)
async def upload_credit_report(
    file: UploadFile = UploadFile(..., description="Credit report file (PDF or text)")
) -> Dict[str, Any]:
    """
    Process a credit report file and return structured data.
    
    Args:
        file (UploadFile): The file to process
        
    Returns:
        dict: Structured credit report data
        
    Raises:
        HTTPException: 
            - 400: Invalid file format or empty file
            - 413: File too large
            - 500: Processing error
    """
    # Validate file format
    if not (file.filename.endswith('.pdf') or file.filename.endswith('.txt')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only PDF and text files are accepted."
        )
    
    try:
        # Create temp file path
        file_path = pdf_service.credit_reports_dir / file.filename
        
        # Save uploaded file
        content = await file.read()
        if not content:
            raise HTTPException(
                status_code=400,
                detail="Empty file provided"
            )
            
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Convert to text
        text_content = pdf_service.convert_pdf_to_text(file.filename, save_output=False)
        
        # Parse text content
        parsed_data = await parser_service.parse_credit_report(text_content)
        
        # Cleanup temp files
        pdf_service.cleanup_temp_files(Path(file.filename).stem)
        
        return JSONResponse(
            content=parsed_data,
            status_code=200
        )
        
    except Exception as e:
        # Ensure cleanup on error
        try:
            pdf_service.cleanup_temp_files(Path(file.filename).stem)
        except:
            pass
            
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the file: {str(e)}"
        )
