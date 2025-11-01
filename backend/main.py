from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from docx import Document
import os

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy skill list for matching
SKILL_KEYWORDS = ["python", "machine learning", "fastapi", "sql", "nlp", "data science", "api", "javascript"]

def extract_text_from_pdf(file_path):
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def analyze_resume_text(text):
    text_lower = text.lower()
    detected_skills = [skill for skill in SKILL_KEYWORDS if skill in text_lower]

    score = len(detected_skills) * 10
    score = min(score, 100)

    return {
        "skills_detected": detected_skills,
        "score": score,
        "analysis_summary": "Keyword-based ATS scoring successful.",
        "recommendation": "For real AI insights, integrate OpenAI/HF API later."
    }

@app.get("/")
def root():
    return {"message": "AI Resume Analyzer Backend Running ✅"}

@app.post("/analyze-resume/")
async def analyze_resume(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)

    with open(file_location, "wb") as f:
        f.write(await file.read())

    if file.filename.lower().endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_location)
    elif file.filename.lower().endswith(".docx"):
        extracted_text = extract_text_from_docx(file_location)
    else:
        return {"error": "Only PDF and DOCX supported"}

    os.remove(file_location)

    result = analyze_resume_text(extracted_text)

    return {
        "status": "success",
        "filename": file.filename,
        "content_preview": extracted_text[:300] + "...",
        "analysis": result
    }
