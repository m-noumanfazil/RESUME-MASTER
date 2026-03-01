import streamlit as st
from classes import ResumeRankingSystem, JobDescription
import os
import pandas as pd

# ---------------------------
# Session State Initialization
# ---------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "hero"  # hero, jd_upload, results

if "system" not in st.session_state:
    st.session_state.system = ResumeRankingSystem()

if "job_processed" not in st.session_state:
    st.session_state.job_processed = False

if "jd_text_saved" not in st.session_state:
    st.session_state.jd_text_saved = ""

if "resumes_analyzed" not in st.session_state:
    st.session_state.resumes_analyzed = False

# ---------------------------
# SIDEBAR RESET CONTROL
# ---------------------------
with st.sidebar:
    st.title("Control Panel")
    if st.button("🔄 Reset Application"):
        st.session_state.current_page = "hero"
        st.session_state.job_processed = False
        st.session_state.jd_text_saved = ""
        st.session_state.resumes_analyzed = False
        st.session_state.system = ResumeRankingSystem()
        st.rerun()

# ---------------------------
# HERO PAGE
# ---------------------------
if st.session_state.current_page == "hero":
    st.title("Transparent Skill-Based Resume Ranking System")
    st.subheader("Explainable 70/30 weighted candidate evaluation — No Black Box AI")

    if st.button("🚀 Get Started"):
        st.session_state.current_page = "jd_upload"
        st.rerun()

# ---------------------------
# JOB DESCRIPTION + RESUME PAGE
# ---------------------------
elif st.session_state.current_page == "jd_upload":

    # Step 1: Job Description Input
    st.header("Step 1: Enter Job Description")
    st.divider()

    jd_text = st.text_area(
        "Paste the Job Description below:",
        value=st.session_state.jd_text_saved,
        height=220,
        disabled=st.session_state.job_processed  # Lock after processing
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if not st.session_state.job_processed:
            if st.button("Analyze Job Description"):
                if jd_text.strip() == "":
                    st.error("Please enter a job description.")
                else:
                    st.session_state.system.job = JobDescription()
                    with st.spinner("Extracting required skills and experience..."):
                        st.session_state.system.job.process_text(jd_text)

                    st.session_state.jd_text_saved = jd_text
                    st.session_state.job_processed = True
                    st.rerun()

    with col2:
        if st.session_state.job_processed:
            if st.button("Edit Job Description"):
                st.session_state.job_processed = False
                st.session_state.system.job = None
                st.rerun()

    # Display Extracted Requirements
    if st.session_state.job_processed:
        job = st.session_state.system.job
        st.success("Job Description processed successfully!")
        st.subheader("Extracted Requirements")
        skills_line = ", ".join(job.skills) if job.skills else "None detected"
        st.write(f"**Required Skills:** {skills_line}")
        st.write(f"**Required Experience:** {job.required_experience} years")

        # Step 2: Resume Upload
        st.divider()
        st.header("Step 2: Upload Resumes & Analyze")
        uploaded_files = st.file_uploader(
            "Upload candidate resumes (PDF only)",
            type=["pdf"],
            accept_multiple_files=True
        )

        if uploaded_files:
            st.write(f"{len(uploaded_files)} file(s) uploaded:")
            for f in uploaded_files:
                st.write(f"- {f.name}")

            if st.button("📊 Analyze Resumes"):
                st.session_state.system.resumes = []

                with st.spinner("Processing resumes and scoring..."):
                    for file in uploaded_files:
                        try:
                            temp_path = f"temp_{file.name}"
                            with open(temp_path, "wb") as f_temp:
                                f_temp.write(file.getbuffer())

                            st.session_state.system.process_resumes([temp_path])
                            os.remove(temp_path)
                        except Exception as e:
                            st.error(f"❌ Error processing {file.name}: {e}")
                            continue

                    try:
                        st.session_state.system.calculate_scores()
                        st.session_state.resumes_analyzed = True  # <- flag set here
                    except Exception as e:
                        st.error(f"❌ Scoring failed: {e}")
                        st.stop()

                st.success("✅ Resumes processed and scored successfully!")

# ---------------------------
# BUTTON TO RESULTS PAGE
# ---------------------------
    if st.session_state.resumes_analyzed:
        if st.button("➡️ Show Ranked Candidates"):
            st.session_state.current_page = "results"
            st.rerun()
    
# ---------------------------
# RESULTS PAGE
# ---------------------------
elif st.session_state.current_page == "results":

    st.header("Step 3: Ranked Candidates")
    st.divider()

    if not st.session_state.system.resumes:
        st.warning("No resumes available. Go back and upload resumes first.")
    else:
        # Prepare table data
        rows = []
        for i, r in enumerate(st.session_state.system.resumes, start=1):
            rows.append({
                "Rank": i,
                "Candidate": r.name,
                "Skill Match (%)": r.skill_match_pct,
                "Experience Match (%)": r.exp_score_pct,
                "Final Score": r.score,
                "Matched Skills": ", ".join(r.matched_skills),
                "Missing Skills": ", ".join(r.missing_skills)
            })
        df = pd.DataFrame(rows)

        # Show main ranking table
        st.subheader("Top Candidates")
        st.dataframe(
            df[["Rank", "Candidate", "Skill Match (%)", "Experience Match (%)", "Final Score"]],
            use_container_width=True
        )

        # Detailed expanders
        st.subheader("Candidate Skill Details")
        for i, r in enumerate(st.session_state.system.resumes, start=1):
            with st.expander(f"{i}. {r.name} - Details"):
                st.write(f"**Matched Skills:** {', '.join(r.matched_skills) if r.matched_skills else 'None'}")
                st.write(f"**Missing Skills:** {', '.join(r.missing_skills) if r.missing_skills else 'None'}")

        # CSV Download
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV of Ranked Candidates",
            data=csv,
            file_name="ranked_candidates.csv",
            mime="text/csv"
        )
        if st.button("⬅️ Back to Job/Resume Page"):
           st.session_state.current_page = "jd_upload"
           st.rerun()