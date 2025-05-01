import PyPDF2
import docx
from io import BytesIO

def parse_resume(file):
    """
    Parse resume file (PDF or DOCX) and extract text content
    """
    filename = file.filename.lower()
    
    if filename.endswith('.pdf'):
        return parse_pdf(file)
    elif filename.endswith('.docx'):
        return parse_docx(file)
    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX files.")

def parse_job_description(file):
    """
    Parse job description file (PDF or DOCX) and extract text content
    """
    return parse_resume(file)  # Reuse the same parsing logic

def parse_pdf(file):
    """
    Extract text from PDF file
    """
    pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def parse_docx(file):
    """
    Extract text from DOCX file
    """
    doc = docx.Document(BytesIO(file.read()))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text 