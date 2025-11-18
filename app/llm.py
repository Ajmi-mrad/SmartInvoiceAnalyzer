import google.generativeai as genai
import os
import json
import logging

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def analyze_invoice_text(text: str) -> dict:
    """Extract invoice data using Gemini"""
    
    prompt = f"""
    Extract invoice information from this text and return JSON:
    
    {text}
    
    Return only this JSON structure:
    {{
        "supplier": "company name",
        "total_amount": 0.0,
        "invoice_number": "number or null",
        "summary": "brief description"
    }}
    
    If you can't find a field, use null or 0.0. Return only JSON.
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean response
        if response_text.startswith("```json"):
            response_text = response_text[7:-3]
        
        return json.loads(response_text)
        
    except Exception as e:
        logger.error(f"LLM failed: {e}")
        return {
            "supplier": "Unknown",
            "total_amount": 0.0,
            "invoice_number": None,
            "summary": f"AI Error: {str(e)}"
        }