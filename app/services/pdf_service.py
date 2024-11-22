import os
import uuid
from fastapi import UploadFile
from typing import Dict, Any
from app.core.config import settings
from app.utils.pdf_utils import get_pdf_info, extract_bbox_content

class PDFService:
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)
        # Create directory for extracted images
        self.images_dir = os.path.join(self.upload_dir, "images")
        os.makedirs(self.images_dir, exist_ok=True)

    async def process_pdf(self, file: UploadFile) -> Dict[str, Any]:
        """
        Process the uploaded PDF file
        """
        try:
            pdf_id = str(uuid.uuid4())
            filename = f"{pdf_id}_{file.filename}"
            file_path = os.path.join(self.upload_dir, filename)
            
            # Save the uploaded file
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            # Get PDF info
            pdf_info = get_pdf_info(self.upload_dir, pdf_id)
            if not pdf_info:
                raise Exception("Failed to process PDF")
                
            _, pdf_name, page_count = pdf_info
            
            return {
                "pdf_id": pdf_id,
                "filename": file.filename,
                "page_count": page_count,
                "status": "processed"
            }
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    async def get_pdf_status(self, pdf_id: str) -> Dict[str, Any]:
        """
        Get the status and data of a processed PDF
        """
        try:
            pdf_info = get_pdf_info(self.upload_dir, pdf_id)
            if not pdf_info:
                raise Exception("PDF not found")
                
            filename, pdf_name, page_count = pdf_info
            
            return {
                "pdf_id": pdf_id,
                "filename": filename,
                "page_count": page_count,
                "status": "completed"
            }
        except Exception as e:
            raise Exception(f"Error getting PDF status: {str(e)}")

    async def extract_region(self, pdf_id: str, page_num: int, bbox_data: Dict[str, float]) -> Dict[str, Any]:
        """
        Extract content from a specific region of a PDF page
        """
        try:
            pdf_info = get_pdf_info(self.upload_dir, pdf_id)
            if not pdf_info:
                raise Exception("PDF not found")
                
            filename, pdf_name, _ = pdf_info
            
            result = extract_bbox_content(
                filename,
                pdf_name,
                page_num,
                bbox_data["x"],
                bbox_data["y"],
                bbox_data["width"],
                bbox_data["height"]
            )
            
            return result
        except Exception as e:
            raise Exception(f"Error extracting region: {str(e)}")

pdf_service = PDFService() 