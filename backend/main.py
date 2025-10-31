from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import docx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ✅ Allow frontend ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Dummy AI analyzer function
def analyze_resume_text(text: str):
    # Later we will integrate real AI
    return {
        "skills_detected": ["Python", "Machine Learning", "FastAPI", "NLP"],
        "analysis_summary": "Candidate has strong technical background and AI skills.",
        "recommendation": "Great fit for AI/ML roles."
    }

# ✅ Extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# ✅ Extract text from DOCX
def extract_text_from_docx(file_path):
    text = ""
    doc = docx.Document(file_path)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# ✅ Backend test route
@app.get("/")
async def root():
    return {"message": "Backend running successfully ✅"}

# ✅ Resume Upload Route
@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):

    file_location = f"temp_{file.filename}"

    # Save uploaded file
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # ✅ Extract text based on file type
    if file.filename.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_location)
    elif file.filename.endswith(".docx"):
        extracted_text = extract_text_from_docx(file_location)
    else:
        return {"error": "File format not supported. Upload PDF or DOCX"}

    # ✅ Analyze text using dummy AI
    result = analyze_resume_text(extracted_text)

    # Delete file after processing
    os.remove(file_location)

    return {
        "status": "success",
        "filename": file.filename,
        "content_preview": extracted_text[:300] + "...",  # Showing first 300 chars
        "analysis": result
    }
