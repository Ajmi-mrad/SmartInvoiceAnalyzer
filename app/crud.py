from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, utils

def create_user(db: Session, user: schemas.UserCreate):
    hashed = utils.hash_password(user.password)
    db_user = models.User(username=user.username, password_hash=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_invoice(db: Session, user_id: int, invoice: schemas.InvoiceCreate):
    db_invoice = models.Invoice(**invoice.dict(), user_id=user_id)
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_invoice(db: Session, invoice_id: int):
    return db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

def update_invoice(db: Session, invoice_id: int, invoice_update: schemas.InvoiceCreate, user_id: int = None):
    """Update an existing invoice with authorization check"""
    
    db_invoice = get_invoice(db, invoice_id)
    
    if not db_invoice:
        return None  # Invoice not found
    
    # Optional: Check authorization at CRUD level
    if user_id and db_invoice.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this invoice")
    
    # Update fields
    db_invoice.supplier = invoice_update.supplier
    db_invoice.total_amount = invoice_update.total_amount
    
    if invoice_update.file_path is not None:
        db_invoice.file_path = invoice_update.file_path
    
    db.commit()
    db.refresh(db_invoice)
    
    return db_invoice

def delete_invoice(db: Session, invoice_id: int, user_id: int = None):
    """Delete an invoice with authorization check"""
    db_invoice = get_invoice(db, invoice_id)
    
    if not db_invoice:
        return False  # Invoice not found
    
    # Optional: Check authorization at CRUD level
    if user_id and db_invoice.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this invoice")
    
    db.delete(db_invoice)
    db.commit()
    return True