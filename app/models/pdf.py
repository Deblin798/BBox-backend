from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class PDFBase(BaseModel):
    filename: str
    status: str

class PDFCreate(PDFBase):
    pass

class PDFResponse(PDFBase):
    id: str
    page_count: int
    created_at: datetime = datetime.now()
    processed_at: Optional[datetime] = None
    extracted_data: Optional[Dict[str, Any]] = None

class BBoxData(BaseModel):
    x: float
    y: float
    width: float
    height: float
    page_num: int