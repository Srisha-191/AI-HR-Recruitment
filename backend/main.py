import os
from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader
from transformers import pipeline
import uvicorn

app = FastAPI()

# Load summarizer once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.get("/")
def home():
    return {"message": "AI HR Recruitment backend is running with NLP!"}

@app.post("/analyze_resume/")
async def analyze_resume(file: UploadFile = File(...)):
    pdf_reader = PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    text = text[:2000]

    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']

    keywords = []
    for word in ["Python", "Java", "SQL", "Machine Learning", "AI", "Data", "Cloud", "React", "Node", "Communication"]:
        if word.lower() in text.lower():
            keywords.append(word)

    return {
        "filename": file.filename,
        "summary": summary,
        "skills_detected": keywords,
    }

# ✅ For Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
