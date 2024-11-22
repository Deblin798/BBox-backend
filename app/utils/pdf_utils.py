import os
import fitz  # PyMuPDF
from PIL import Image
from typing import Tuple, Optional, Dict, Any

def get_pdf_info(upload_dir: str, pdf_id: str) -> Optional[Tuple[str, str, int]]:
    """
    Get information about a PDF file
    """
    try:
        # Find the PDF file corresponding to the pdf_id
        pdf_files = [f for f in os.listdir(upload_dir) if f.startswith(pdf_id) and f.endswith('.pdf')]
        if not pdf_files:
            return None
            
        pdf_filename = pdf_files[0]
        pdf_name = os.path.splitext(pdf_filename)[0]
        pdf_path = os.path.join(upload_dir, pdf_filename)
        
        # Get page count using PyMuPDF
        with fitz.open(pdf_path) as pdf_document:
            page_count = pdf_document.page_count
            
        return pdf_filename, pdf_name, page_count
    except Exception as e:
        print(f"Error getting PDF info: {str(e)}")
        return None

def extract_bbox_content(filename: str, pdf_name: str, page_num: int, 
                        x: float, y: float, width: float, height: float) -> Dict[str, Any]:
    """
    Extract content from a specific area of a PDF page
    """
    try:
        pdf_path = os.path.join("uploads", filename)
        with fitz.open(pdf_path) as pdf_document:
            page = pdf_document.load_page(page_num - 1)
            
            # Define the bounding box
            bbox = fitz.Rect(x, y, x + width, y + height)
            
            # Extract text from the region
            text = page.get_text("text", clip=bbox)
            
            # Get image from the region
            pix = page.get_pixmap(clip=bbox)
            
            # Save the image
            image_dir = os.path.join("uploads", "images", pdf_name)
            os.makedirs(image_dir, exist_ok=True)
            image_filename = f"page_{page_num}_x{int(x)}_y{int(y)}.png"
            image_path = os.path.join(image_dir, image_filename)
            pix.save(image_path)
            
            return {
                "text": text,
                "image_path": image_path,
                "page": page_num,
                "coordinates": {
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height
                }
            }
    except Exception as e:
        raise Exception(f"Error extracting content: {str(e)}") 