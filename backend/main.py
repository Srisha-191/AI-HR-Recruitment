from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader
from transformers import pipeline

app = FastAPI()

# Load a summarization pipeline once at startup
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.get("/")
def home():
    return {"message": "AI HR Recruitment backend is running with NLP!"}

@app.post("/analyze_resume/")
async def analyze_resume(file: UploadFile = File(...)):
    # Step 1: Extract text from PDF
    pdf_reader = PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    # Limit text for processing (avoid overload)
    text = text[:2000]

    # Step 2: Summarize the resume
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']

    # Step 3: Extract keywords (simple rule-based for now)
    keywords = []
    for word in ["Python", "Java", "SQL", "Machine Learning", "AI", "Data", "Cloud", "React", "Node", "Communication"]:
        if word.lower() in text.lower():
            keywords.append(word)

    return {
        "filename": file.filename,
        "summary": summary,
        "skills_detected": keywords,
    }
