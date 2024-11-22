from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import pdf_service
from app.models.pdf import BBoxData
from typing import Dict, Any

router = APIRouter()

@router.get("/test")
async def test_endpoint():
    """
    Test endpoint to verify API is working
    """
    return {
        "status": "success",
        "message": "API is working properly",
        "service": "PDF Extractor"
    }

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file for processing
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        result = await pdf_service.process_pdf(file)
        return {"message": "PDF processed successfully", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{pdf_id}")
async def get_pdf_status(pdf_id: str):
    """
    Get the processing status and data of a PDF
    """
    try:
        status = await pdf_service.get_pdf_status(pdf_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{pdf_id}/extract")
async def extract_bbox(pdf_id: str, bbox_data: BBoxData):
    """
    Extract content from a specific area of a PDF page
    """
    try:
        result = await pdf_service.extract_region(
            pdf_id,
            bbox_data.page_num,
            bbox_data.dict(exclude={'page_num'})
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 