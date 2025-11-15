from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Data Validation & API Contracts (Pydantic Models for request/response bodies)
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class InvoiceCreate(BaseModel):
    supplier: str
    total_amount: float
    file_path: Optional[str] = None

class InvoiceOut(BaseModel):
    id: int
    supplier: str
    total_amount: float
    upload_date: datetime
    
    class Config:
        from_attributes = True
