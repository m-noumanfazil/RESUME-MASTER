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
        self.required_experience = 0.0
        self.raw_text = ""
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Backend-only function: just process whatever text is passed
    def process_text(self, raw_text: str):
        self.raw_text = raw_text.strip()
        if not self.raw_text:
            print("❌ No Job Description text provided.")
            self.skills = []
            self.required_experience = 0.0
            return

        prompt = f"""
        You are a strict data extraction engine.
        
        Extract ONLY:
        1. A list of required technical skills.
        2. Total required professional experience in years (decimal allowed).
        
        Return ONLY valid JSON.
        No explanation.
        No markdown.
        No extra text.
        
        Format exactly like this:
        {{
          "skills": ["skill1", "skill2"],
          "experience_years": 3.0 
        }}
        
        If experience is not mentioned, return 0.0.
        If no skills found, return an empty list.
        
        Job Description:
        \"\"\"{self.raw_text}\"\"\"
        """

        try:
            response = self.client.chat.completions.create(
                model="qwen/qwen3-32b",
                temperature=0,
                messages=[
                    {"role": "system", "content": "You extract structured job requirement information."},
                    {"role": "user", "content": prompt}
                ],
                reasoning_effort="none"
            )

            output_text = response.choices[0].message.content.strip()
            result = json.loads(output_text)

            skills = result.get("skills", [])
            experience = result.get("experience_years", 0)

            if not isinstance(skills, list):
                skills = []

            if not isinstance(experience, (int, float)):
                experience = 0

            self.skills = [canonicalize_skill(normalize_skill(s)) for s in skills]
            self.required_experience = round(float(experience), 1)

            print("✅ Job Description processed successfully!")
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
    def process_resumes(self, paths: list):
        if self.job is None:
            print("❌ Please insert a Job Description first!")
            return
    
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
        
                prompt = f"""
                        Extract ONLY:
                        1. All technical skills (from Skills section and project tools mentioned in the resume).
                        2. Total professional experience in years (decimal allowed, e.g., 2.5 for 2 years 6 months).
                        
                        Return ONLY valid JSON in this exact format:
                        {{
                            "skills": ["skill1", "skill2"],
                            "experience_years": 0.0
                        }}
                        
                        NO explanations, NO markdown, NO extra text, NO thoughts.
                        
                        Resume text:
                    \"\"\"{text_clean}\"\"\"
                    """
        
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
        
                output_text = re.sub(r"<think>.*?</think>", "", output_text, flags=re.DOTALL).strip()
        
                if not output_text.startswith("{"):
                    raise ValueError("AI output is not valid JSON. Check the model response.")
        
                result = json.loads(output_text)
        
                skills = [canonicalize_skill(normalize_skill(s)) for s in result.get("skills", [])]
                experience = result.get("experience_years", 0)
                try:
                    experience = round(float(experience), 1)
                except:
                    experience = 0.0
        
                resume_name = os.path.basename(path)
                self.resumes.append(
                    Resume(name=resume_name, skills=skills, experience=experience)
                )
        
                print(f"✅ Processed: {resume_name}")
                print(f"   Skills: {skills}")
                print(f"   Experience: {experience} years")
        
            except Exception as e:
                print(f"❌ Error processing {path}: {e}")
    # Inside ResumeRankingSystem class

    def calculate_scores(self):
        if self.job is None:
            raise ValueError("Please insert a Job Description first!")
    
        if not self.resumes:
            raise ValueError("No resumes to score!")
    
        for resume in self.resumes:
            required_skills = set(self.job.skills)
            candidate_skills = set(resume.skills)
            
            matched_skills = required_skills.intersection(candidate_skills)
            missing_skills = required_skills - matched_skills
            
            skill_match_pct = (
                len(matched_skills) / len(required_skills) * 100
                if required_skills else 0
            )
    
            if self.job.required_experience > 0:
                exp_ratio = resume.experience / self.job.required_experience
                exp_score_pct = min(exp_ratio * 100, 100)
            else:
                exp_score_pct = 0.0
    
            final_score = skill_match_pct * 0.7 + exp_score_pct * 0.3
    
            resume.skill_match_pct = round(skill_match_pct, 1)
            resume.exp_score_pct = round(exp_score_pct, 1)
            resume.score = round(final_score, 1)
    
            resume.matched_skills = list(matched_skills)
            resume.missing_skills = list(missing_skills)
    
        self.resumes.sort(
            key=lambda r: (r.score, r.skill_match_pct, r.exp_score_pct),
            reverse=True
        )
    
        return self.resumes
    
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