from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from . import database, models, schemas, crud, utils, auth, ocr, llm
import tempfile
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Smart Invoice Analyzer")

@app.post("/auth/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return crud.create_user(db, user)

@app.post("/auth/login")
def login(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    
    if not db_user or not utils.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = auth.create_access_token({"sub": db_user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": schemas.UserOut.model_validate(db_user)  # Fixed this line
    }

@app.post("/invoices/", response_model=schemas.InvoiceOut)
def create_invoice(invoice: schemas.InvoiceCreate, current_user=Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    return crud.create_invoice(db, current_user.id, invoice)

@app.get("/invoices/", response_model=list[schemas.InvoiceOut])
def list_invoices(current_user=Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    return db.query(models.Invoice).filter(models.Invoice.user_id == current_user.id).all()


@app.get("/invoices/{invoice_id}", response_model=schemas.InvoiceOut)
def get_invoice(
    invoice_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Get a specific invoice by ID"""
    invoice = crud.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Check if invoice belongs to current user
    if invoice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this invoice")
    
    return invoice

@app.put("/invoices/{invoice_id}", response_model=schemas.InvoiceOut)
def update_invoice(
    invoice_id: int,
    invoice_update: schemas.InvoiceCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Update an invoice"""
    # Single function call, single database query
    updated_invoice = crud.update_invoice(db, invoice_id, invoice_update, current_user.id)
    
    if not updated_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    return updated_invoice

@app.post("/invoices/upload")
async def upload_invoice_pdf(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Upload PDF invoice and extract data with enhanced OCR"""
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    try:
        # Read PDF
        pdf_content = await file.read()
        
        if len(pdf_content) == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Enhanced OCR extraction
        logger.info(f"Starting enhanced OCR extraction for {file.filename}")
        extraction_result = ocr.extract_pdf_auto(pdf_content)
        
     
        # Check if extraction was successful
        if not extraction_result["extraction_successful"]:
            logger.warning(f"OCR extraction had issues: {extraction_result['text']}")
        
        extracted_text = extraction_result["text"]
        logger.info(f"Enhanced OCR extracted {len(extracted_text)} characters using {extraction_result['pdf_type']} method")
        llm_data = llm.analyze_invoice_text(extracted_text)
        return llm_data  
        
    except Exception as e:
        logger.error(f"Upload processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
