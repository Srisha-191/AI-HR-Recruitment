from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF for PDF extraction
import docx
import io
import re

app = FastAPI()

# Allow frontend connection (React at localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Function: Extract text from PDF ---
def extract_text_from_pdf(file_bytes):
    text = ""
    pdf = fitz.open(stream=file_bytes, filetype="pdf")
    for page in pdf:
        text += page.get_text("text")
    return text.strip()

# --- Function: Extract text from DOCX ---
def extract_text_from_docx(file_bytes):
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join([p.text for p in doc.paragraphs])

# --- Function: Extract skills intelligently ---
def extract_skills(text):
    # List of common skills and technologies
    skills = [
        "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "React", "Angular", "Vue",
        "HTML", "CSS", "Node.js", "Express", "Django", "Flask", "FastAPI",
        "SQL", "PostgreSQL", "MySQL", "MongoDB", "Firebase",
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Git", "GitHub",
        "REST API", "GraphQL", "Machine Learning", "Deep Learning", "Data Analysis",
        "Pandas", "NumPy", "TensorFlow", "PyTorch", "OpenCV", "NLP",
        "Excel", "Power BI", "Tableau", "Bootstrap", "Tailwind", "jQuery"
    ]

    found_skills = []
    text_lower = text.lower()
    for skill in skills:
        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text_lower):
            found_skills.append(skill)

    return list(set(found_skills)) if found_skills else ["N/A"]

# --- Function: Calculate a simple score ---
def calculate_score(skills):
    if "N/A" in skills:
        return 30
    return min(100, 30 + len(skills) * 3)  # simple scoring formula

# --- API Route ---
@app.post("/analyze-resume/")
async def analyze_resume(file: UploadFile = File(...)):
    file_bytes = await file.read()

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file_bytes)
    else:
        return {"error": "Unsupported file format"}

    skills = extract_skills(text)
    score = calculate_score(skills)

    preview = text[:500].replace("\n", " ")

    return {
        "score": score,
        "skills": skills,
        "preview": preview
    }

@app.get("/")
def root():
    return {"message": "AI Resume Analyzer API is running"}
