from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from classes import ResumeRankingSystem, JobDescription
import os
from typing import List

app = FastAPI(title="Smart Resume Filter API")

# ------------------- CORS -------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # your Next.js frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Global System -------------------
system = ResumeRankingSystem()
current_job: JobDescription | None = None

# ------------------- Analyze Job Description -------------------
@app.post("/analyze-job")
async def analyze_job(jd_text: str = Form(...)):
    global system, current_job
    current_job = JobDescription()
    current_job.process_text(jd_text)
    system.job = current_job
    return {
        "message": "Job Description processed successfully",
        "skills": current_job.skills,
        "required_experience": current_job.required_experience,
    }

# ------------------- Upload Resumes -------------------
@app.post("/upload-resumes")
async def upload_resumes(files: List[UploadFile] = File(...)):
    if current_job is None:
        return {"error": "Please analyze a Job Description first."}

    temp_paths = []

    # Save uploaded resumes temporarily
    for file in files:
        path = f"{file.filename}"
        with open(path, "wb") as f:
            f.write(await file.read())
        temp_paths.append(path)

    # Process resumes
    system.resumes = []  # reset
    system.process_resumes(temp_paths)
    system.calculate_scores()

    # Cleanup temp files
    for path in temp_paths:
        os.remove(path)

    # Prepare JSON response
    ranked_candidates = []
    for idx, r in enumerate(system.resumes, start=1):
        ranked_candidates.append({
            "Rank": idx,
            "Candidate": r.name,
            "Skill Match (%)": r.skill_match_pct,
            "Experience Match (%)": r.exp_score_pct,
            "Final Score": r.score,
            "Matched Skills": ", ".join(r.matched_skills),
            "Missing Skills": ", ".join(r.missing_skills)
        })

    return {"ranked_candidates": ranked_candidates, "message": "Resumes processed successfully"}