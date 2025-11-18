import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import logging
import tempfile
import os
from typing import Dict, List

logger = logging.getLogger(__name__)

def extract_text_pymupdf(pdf_bytes: bytes) -> str:
    """Extract text from a digital PDF (non-scanned)."""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        full_text = ""

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            
            if page_num > 0:
                full_text += f"\n\n--- PAGE {page_num + 1} ---\n\n"
            full_text += text

        doc.close()
        logger.info(f" Digital PDF: Extracted {len(full_text)} characters")
        return full_text.strip()
        
    except Exception as e:
        logger.error(f"PyMuPDF extraction failed: {str(e)}")
        return f"ERROR: PyMuPDF extraction failed - {str(e)}"

def extract_text_ocr(pdf_bytes: bytes) -> str:
    """Extract text from a scanned PDF using OCR."""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        full_text = ""

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            
            # Convert page to high-quality image
            pix = page.get_pixmap(dpi=300)
            img_bytes = pix.tobytes()
            img = Image.open(io.BytesIO(img_bytes))

            # OCR with Tesseract
            logger.info(f"Running OCR on page {page_num + 1}")
            text = pytesseract.image_to_string(img, config='--psm 6')
            
            if page_num > 0:
                full_text += f"\n\n--- PAGE {page_num + 1} (OCR) ---\n\n"
            full_text += text

        doc.close()
        logger.info(f"✅ OCR PDF: Extracted {len(full_text)} characters")
        return full_text.strip()
        
    except Exception as e:
        logger.error(f"OCR extraction failed: {str(e)}")
        return f"ERROR: OCR extraction failed - {str(e)}"

def is_scanned_page(page) -> bool:
    """Return True if the page has no selectable text."""
    extracted = page.get_text().strip()
    return len(extracted) < 10  # Less than 10 characters = likely scanned

def extract_pdf_auto(pdf_bytes: bytes) -> Dict:
    """
    Auto-detect if PDF is digital or scanned.
    Returns structured result.
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # Check if PDF is scanned by examining first few pages
        scanned_pages = 0
        pages_to_check = min(3, doc.page_count)  # Check max 3 pages
        
        for page_num in range(pages_to_check):
            page = doc.load_page(page_num)
            if is_scanned_page(page):
                scanned_pages += 1
        
        # If more than half the checked pages are scanned, treat as scanned PDF
        is_scanned = scanned_pages > (pages_to_check / 2)
        
        doc.close()
        
        # Extract text based on detection
        if is_scanned:
            text = extract_text_ocr(pdf_bytes)
            pdf_type = "scanned"
            logger.info(f"📄 Detected: Scanned PDF - using OCR")
        else:
            text = extract_text_pymupdf(pdf_bytes)
            pdf_type = "digital"
            logger.info(f"📄 Detected: Digital PDF - using direct extraction")
        
        # Re-open to get page count for metadata
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page_count = doc.page_count
        doc.close()
        
        return {
            "pdf_type": pdf_type,
            "text": text,
            "page_count": page_count,
            "character_count": len(text),
            "word_count": len(text.split()) if text else 0,
            "extraction_successful": not text.startswith("ERROR:")
        }
        
    except Exception as e:
        logger.error(f"Auto PDF extraction failed: {str(e)}")
        return {
            "pdf_type": "unknown",
            "text": f"ERROR: Auto extraction failed - {str(e)}",
            "page_count": 0,
            "character_count": 0,
            "word_count": 0,
            "extraction_successful": False
        }
