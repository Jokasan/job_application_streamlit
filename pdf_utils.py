"""
PDF parsing utilities for extracting text from CV files.
"""

import PyPDF2
from io import BytesIO
import streamlit as st


def extract_text_from_pdf(pdf_file):
    """
    Extract text from an uploaded PDF file.
    
    Args:
        pdf_file: Streamlit uploaded file object
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
        
        # Extract text from all pages
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        
        # Clean up the text (remove extra whitespace, normalize line breaks)
        text = " ".join(text.split())
        
        return text
    
    except Exception as e:
        st.error(f"Error reading PDF file: {str(e)}")
        return None


def validate_pdf_content(text):
    """
    Validate that the extracted PDF content is meaningful for a CV.
    
    Args:
        text (str): Extracted text from PDF
        
    Returns:
        bool: True if content appears to be a valid CV, False otherwise
    """
    if not text or len(text.strip()) < 100:
        return False
    
    # Check for common CV keywords (case insensitive)
    cv_keywords = [
        'experience', 'education', 'skills', 'work', 'employment',
        'degree', 'university', 'college', 'certificate', 'qualification',
        'project', 'responsibility', 'achievement', 'contact', 'email'
    ]
    
    text_lower = text.lower()
    keyword_count = sum(1 for keyword in cv_keywords if keyword in text_lower)
    
    # If at least 3 CV-related keywords are found, consider it valid
    return keyword_count >= 3
