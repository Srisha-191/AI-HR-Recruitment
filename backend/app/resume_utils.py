from PyPDF2 import PdfReader
from docx import Document
from fastapi import HTTPException

SKILL_KEYWORDS = ["python", "machine learning", "fastapi", "sql", "nlp", "data science", "api", "javascript"]

def extract_pdf(path):
    try:
        reader = PdfReader(path)
        return "".join([page.extract_text() or "" for page in reader.pages])
    except:
        raise HTTPException(status_code=500, detail="Error reading PDF")

def extract_docx(path):
    try:
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    except:
        raise HTTPException(status_code=500, detail="Error reading DOCX")
