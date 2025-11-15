from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    invoices = relationship("Invoice", back_populates="user")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String)
    # supplier: Company that sent the invoice
    supplier = Column(String)
    total_amount = Column(Float)
    upload_date = Column(DateTime, default=datetime.utcnow)
    # user_id: Reference to the user who uploaded the invoice
    user_id = Column(Integer, ForeignKey("users.id"))

    # Each invoice belongs to one user
    user = relationship("User", back_populates="invoices")
