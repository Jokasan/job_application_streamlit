"""
PDF generation utilities for creating downloadable cover letters.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black
from io import BytesIO
import re


def create_cover_letter_pdf(cover_letter_text, applicant_name="[Your Name]"):
    """
    Create a PDF from the cover letter text.
    
    Args:
        cover_letter_text (str): The cover letter content
        applicant_name (str): Name of the applicant
        
    Returns:
        bytes: PDF file as bytes
    """
    # Create a BytesIO buffer to store the PDF
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        textColor=black,
        alignment=1  # Center alignment
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        leading=14,
        textColor=black,
        alignment=0  # Left alignment
    )
    
    # Build the PDF content
    story = []
    
    # Add title
    story.append(Paragraph("Cover Letter", title_style))
    story.append(Spacer(1, 20))
    
    # Clean and format the cover letter text
    # Split by double newlines to preserve paragraph structure
    paragraphs = re.split(r'\n\s*\n', cover_letter_text.strip())
    
    for paragraph in paragraphs:
        if paragraph.strip():
            # Clean up the paragraph text
            clean_paragraph = paragraph.strip().replace('\n', ' ')
            # Remove excessive whitespace
            clean_paragraph = re.sub(r'\s+', ' ', clean_paragraph)
            
            # Add the paragraph to the story
            story.append(Paragraph(clean_paragraph, body_style))
            story.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(story)
    
    # Get the PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data


def format_filename(applicant_name="Your_Name"):
    """
    Create a clean filename for the PDF.
    
    Args:
        applicant_name (str): Name of the applicant
        
    Returns:
        str: Formatted filename
    """
    # Clean the name for filename use
    clean_name = re.sub(r'[^\w\s-]', '', applicant_name)
    clean_name = re.sub(r'[-\s]+', '_', clean_name)
    
    if clean_name.lower() in ['[your name]', 'your_name', '']:
        clean_name = "Cover_Letter"
    else:
        clean_name = f"{clean_name}_Cover_Letter"
    
    return f"{clean_name}.pdf"
