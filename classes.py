# classes.py
# classes.py
# classes.py
# classes.py
import os
import re
from groq import Groq
from dotenv import load_dotenv
import json
import fitz
# load variables from .env file
load_dotenv()

CANONICAL_MAP = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "react js": "react",
    "reactjs": "react",
    "node js": "nodejs",
    "js": "javascript",
    "py": "python"
}

def normalize_skill(skill):
    skill = skill.lower().strip()

    # Remove dots (node.js → nodejs)
    skill = skill.replace(".", "")

    # Remove commas
    skill = skill.replace(",", "")

    # Remove hyphens (react-js → react js)
    skill = skill.replace("-", " ")

    # Collapse multiple spaces
    skill = re.sub(r"\s+", " ", skill)

    # Fix common spacing issues around symbols
    skill = skill.replace(" + +", "++")
    skill = skill.replace(" #", "#")

    return skill

def canonicalize_skill(skill):
    if skill in CANONICAL_MAP:
        return CANONICAL_MAP[skill]
    return skill

class JobDescription:
    def __init__(self):
        self.skills = []
        self.required_experience = 0
        self.raw_text = ""
        # Get Groq API key from environment
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    

    def insert_text(self):
        print("\nPaste the Job Description text below (end with empty line):")
        lines = []
        while True:
            line = input()
            if not line.strip():
                break
            lines.append(line)
    
        self.raw_text = " ".join(lines)
    
        prompt = f"""
    You are a strict data extraction engine.
    
    Extract ONLY:
    1. A list of required technical skills.
    2. Total required professional experience in years (integer).
    
    Return ONLY valid JSON.
    No explanation.
    No markdown.
    No extra text.
    
    Format exactly like this:
    
    {{
      "skills": ["skill1", "skill2"],
      "experience_years": 3
    }}
    
    If experience is not mentioned, return 0.
    If no skills found, return empty list.
    
    Job Description:
    \"\"\"{self.raw_text}\"\"\"
    """
    
        try:
            response = self.client.chat.completions.create(
                model="qwen/qwen3-32b",
                temperature=0,   # VERY IMPORTANT
                messages=[
                    {"role": "system", "content": "You extract structured job requirement information."},
                    {"role": "user", "content": prompt}
                ],
                reasoning_effort="none"
            )
            
            output_text = response.choices[0].message.content.strip()
            #print("RAW MODEL OUTPUT:")
            #print(output_text)
            # Parse safely
            result = json.loads(output_text)
    
            # Validate structure
            skills = result.get("skills", [])
            experience = result.get("experience_years", 0)
    
            if not isinstance(skills, list):
                skills = []
    
            if not isinstance(experience, (int, float)):
                experience = 0
    
            self.skills = [canonicalize_skill(normalize_skill(s)) for s in skills]
            self.required_experience = int(experience)



            print("Normalized JD skills:", self.skills)
            print("Required experience (years):", self.required_experience)
    
            print("\n✅ Job Description processed successfully!")
            print("Extracted skills:", self.skills)
            print("Required experience (years):", self.required_experience)
    
        except Exception as e:
            print("❌ Error processing Job Description:", str(e))
            self.skills = []
            self.required_experience = 0

       

class Resume:
    def __init__(self, name, skills, experience):
        self.name = name
        self.skills = skills
        self.experience = experience
        self.score = 0.0
        self.skill_match_pct = 0.0  # initialize
        self.exp_score_pct = 0.0    # initialize
        # NEW: transparency fields
        self.matched_skills = []
        self.missing_skills = []

class ResumeRankingSystem:
    def __init__(self):
        self.job = None
        self.resumes = []
    def insert_resumes(self):
        if self.job is None:
            print("❌ Please insert a Job Description first!")
            return
    
        # 1️⃣ Collect all resume paths at once
        print("\nEnter path(s) to PDF resume(s), separated by commas:")
        paths = input().split(",")
        paths = [p.strip() for p in paths if p.strip()]
    
        if not paths:
            print("❌ No valid paths entered.")
            return
    
        for path in paths:
            if not os.path.isfile(path):
                print(f"❌ File not found: {path}")
                continue
        
            try:
                # Extract text from PDF
                doc = fitz.open(path)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
        
                # Clean text
                text_clean = re.sub(r'\s+', ' ', text).strip()
        
                # Strict JSON extraction prompt
                prompt = f"""
        Extract ONLY:
        1. All technical skills (from Skills section and project tools mentioned).
        2. Total professional experience in years (integer).
        
        Return ONLY valid JSON in the exact format:
        {{
            "skills": ["skill1", "skill2"],
            "experience_years": 0
        }}
        
        NO explanations, NO markdown, NO extra text, NO thoughts.
        
        Resume text:
        \"\"\"{text_clean}\"\"\"
        """
        
                # AI call
                response = self.job.client.chat.completions.create(
                    model="qwen/qwen3-32b",
                    temperature=0,
                    messages=[
                        {"role": "system", "content": "Extract structured resume info."},
                        {"role": "user", "content": prompt}
                    ],
                    reasoning_effort="none"
                )
        
                output_text = response.choices[0].message.content.strip()
        
                # Remove <think> blocks if any
                output_text = re.sub(r"<think>.*?</think>", "", output_text, flags=re.DOTALL).strip()
        
                # Safety check: must start with '{'
                if not output_text.startswith("{"):
                    raise ValueError("AI output is not valid JSON. Check the model response.")
        
                # Parse JSON
                result = json.loads(output_text)
        
                skills = [s.lower().strip() for s in result.get("skills", [])]
                experience = result.get("experience_years", 0)
        
                # Store in resumes list
                resume_name = os.path.basename(path)
                self.resumes.append(Resume(name=resume_name, skills=skills, experience=experience))
        
                print(f"✅ Processed: {resume_name}")
                print(f"   Skills: {skills}")
                print(f"   Experience: {experience} years")
        
            except Exception as e:
                print(f"❌ Error processing {path}: {e}")
    # Inside ResumeRankingSystem class

    def calculate_scores(self):
        if self.job is None:
            print("❌ Please insert a Job Description first!")
            return
    
        if not self.resumes:
            print("❌ No resumes to score!")
            return
    
        print("\nCalculating scores for all candidates...")
        for resume in self.resumes:
            required_skills = set(self.job.skills)
            candidate_skills = set(resume.skills)
            
            matched_skills = required_skills.intersection(candidate_skills)
            missing_skills = required_skills - matched_skills
            
            # Skill match %
            skill_match_pct = len(matched_skills) / len(required_skills) * 100 if required_skills else 0
            
            # Experience %
            exp_ratio = resume.experience / self.job.required_experience if self.job.required_experience > 0 else 0
            exp_score_pct = min(exp_ratio * 100, 100)
            
            # Weighted final score
            final_score = skill_match_pct * 0.7 + exp_score_pct * 0.3
            
            # Store everything
            resume.skill_match_pct = round(skill_match_pct, 1)
            resume.exp_score_pct = round(exp_score_pct, 1)
            resume.score = round(final_score, 1)
            
            resume.matched_skills = list(matched_skills)
            resume.missing_skills = list(missing_skills)
    
            print(f"✅ {resume.name} | Skill Match: {resume.skill_match_pct}% | Experience Score: {resume.exp_score_pct}% | Final Score: {resume.score}")
    
        # Sort resumes immediately by final score descending
        self.resumes.sort(
            key=lambda r: (r.score, r.skill_match_pct, r.exp_score_pct),
            reverse=True
        )
        print("\n🎯 Scoring completed! Candidates sorted by score.\n\n")
        print("\n--- DEBUG INFO ---")
        print("JD Skills:", required_skills)
        print("Resume Skills:", candidate_skills)
        print("Matched Skills:", matched_skills)
        print("Matched Skills:", missing_skills)
        print("-------------------\n")
    
    def show_sorted_results(self):
        if not self.resumes:
            print("❌ No resumes to display!")
            return
    
        print("\n--- Ranked Candidates ---")
        for i, r in enumerate(self.resumes):
            print(f"{i+1}. {r.name} | Final Score: {r.score} | Skill Match: {r.skill_match_pct}% | Experience: {r.exp_score_pct}%")
            print(f"   Matched Skills: {r.matched_skills}")
            print(f"   Missing Skills: {r.missing_skills}")
        
    def reset_system(self):
        self.job = None
        self.resumes = []
        print("✅ System reset: Job Description and all resumes cleared.")