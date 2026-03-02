import streamlit as st
from classes import ResumeRankingSystem, JobDescription
import os
import pandas as pd
import base64
from pathlib import Path
os.chdir(Path(__file__).parent.parent)
st.set_page_config(page_title="KAABIL-LENS", layout="wide", page_icon="🔍")

st.markdown("""
<style>
/* GET STARTED BUTTON */
div[class*="st-key-get_started_btn"] button {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    color: white !important;
    padding: 14px 36px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    border: 2px solid #F5A623 !important;
    transition: all 0.3s ease !important;
}
div[class*="st-key-get_started_btn"] button:hover {
    background: linear-gradient(90deg, #4AA3F0, #F5A623) !important;
    color: white !important;
    box-shadow: 0px 0px 15px rgba(245, 166, 35, 0.6) !important;
    transform: translateY(-2px) !important;
}

/* ANALYZE JD BUTTON */
div[class*="st-key-analyze_jd_btn"] button {
    background: transparent !important;
    border: 2px solid #4AA3F0 !important;
    color: #F5A623 !important;
    padding: 14px 36px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}
div[class*="st-key-analyze_jd_btn"] button:hover {
    background: transparent !important;
    box-shadow: 0px 0px 12px rgba(245, 166, 35, 0.7) !important;
    border-color: #F5A623 !important;
    color: #F5A623 !important;
    transform: translateY(-2px) !important;
}
/* EDIT JD BUTTON */
div[class*="st-key-edit_jd_btn"] button {
    background: transparent !important;
    border: 2px solid #4AA3F0 !important;
    color: #4AA3F0 !important;
    padding: 14px 36px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}
div[class*="st-key-edit_jd_btn"] button:hover {
    background: transparent !important;
    box-shadow: 0px 0px 12px rgba(74, 163, 240, 0.7) !important;
    border-color: #4AA3F0 !important;
    color: #4AA3F0 !important;
    transform: translateY(-2px) !important;
}
/* Reset button (first button inside sidebar container) */
section[data-testid="stSidebar"] div.stButton:nth-of-type(1) > button {
    background: transparent !important;
    color: #ff4b4b !important;
    border: 2px solid #ff4b4b !important;
    backdrop-filter: none !important;
    font-weight: 600;
    transition: all 0.3s ease;
}
div[class*="st-key-analyze_resumes_btn"] button {
    background: transparent !important;
    border: 2px solid #F5A623 !important;
    color: #4AA3F0 !important;
    padding: 14px 36px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}
div[class*="st-key-analyze_resumes_btn"] button:hover {
    background: transparent !important;
    box-shadow: 0px 0px 12px rgba(74, 163, 240, 0.7) !important;
    border-color: #F5A623 !important;
    color: #4AA3F0 !important;
    transform: translateY(-2px) !important;
}
div[class*="st-key-show_results_btn"] button {
    background: transparent !important;
    border: 2px solid #4AA3F0 !important;
    padding: 14px 36px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: #F5A623 !important;
    border-radius: 12px !important;
    box-shadow: 0px 0px 10px rgba(74, 163, 240, 0.4) !important;
    transition: all 0.3s ease !important;
}
div[class*="st-key-show_results_btn"] button:hover {
    background: transparent !important;
    border-color: #F5A623 !important;
    box-shadow: 0px 0px 15px rgba(245, 166, 35, 0.6), 0px 0px 10px rgba(74, 163, 240, 0.4) !important;
    color: white !important;
    transform: translateY(-2px) !important;
}
div[class*="st-key-back_btn"] button {
    background: transparent !important;
    border: 2px solid #ff4b4b !important;
    color: #ff4b4b !important;
    padding: 14px 36px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    box-shadow: 0px 0px 10px rgba(255, 75, 75, 0.4) !important;
    transition: all 0.3s ease !important;
}
div[class*="st-key-back_btn"] button:hover {
    background: transparent !important;
    border-color: #ff4b4b !important;
    box-shadow: 0px 0px 15px rgba(255, 75, 75, 0.7) !important;
    color: #ff4b4b !important;
    transform: translateY(-2px) !important;
}
section[data-testid="stSidebar"] div.stButton:nth-of-type(1) > button {
    background: transparent !important;
    border: 2px solid #ff4b4b !important;
    color: #ff4b4b !important;
    padding: 14px 36px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    box-shadow: 0px 0px 10px rgba(255, 75, 75, 0.4) !important;
    transition: all 0.3s ease !important;
}
section[data-testid="stSidebar"] div.stButton:nth-of-type(1) > button:hover {
    background: transparent !important;
    border-color: #ff4b4b !important;
    box-shadow: 0px 0px 15px rgba(255, 75, 75, 0.7) !important;
    color: #ff4b4b !important;
    transform: translateY(-2px) !important;
}
div[class*="st-key-download_btn"] button {
    background: transparent !important;
    border: 2px solid #00b894 !important;
    color: #00b894 !important;
    padding: 14px 36px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    box-shadow: 0px 0px 10px rgba(0, 184, 148, 0.4) !important;
    transition: all 0.3s ease !important;
}
div[class*="st-key-download_btn"] button:hover {
    background: transparent !important;
    border-color: #00b894 !important;
    box-shadow: 0px 0px 15px rgba(0, 184, 148, 0.7) !important;
    color: #00b894 !important;
    transform: translateY(-2px) !important;
}
/* Hover effect: subtle glow only */
section[data-testid="stSidebar"] div.stButton:nth-of-type(1) > button:hover {
    /* Keep background transparent */
    background: transparent !important;
    /* Keep text color the same */
    color: #ff4b4b !important;
    /* Add subtle glow */
    box-shadow: 0px 0px 8px rgba(255, 75, 75, 0.5);
    transform: translateY(-2px); /* tiny lift */
}
</style>
""", unsafe_allow_html=True)


# Get the directory where main.py is located
current_dir = Path(__file__).parent
# Go up one level to project root, then into static folder
logo_path = current_dir.parent / "static" / "image.png"
encoded_logo = None
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        encoded_logo = base64.b64encode(f.read()).decode()
# ---------------------------
# Session State Initialization
# ---------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "hero"
if "system" not in st.session_state:
    st.session_state.system = ResumeRankingSystem()
if "job_processed" not in st.session_state:
    st.session_state.job_processed = False
if "jd_text_saved" not in st.session_state:
    st.session_state.jd_text_saved = ""
if "resumes_analyzed" not in st.session_state:
    st.session_state.resumes_analyzed = False
if "csv_downloaded" not in st.session_state:
    st.session_state.csv_downloaded = False
if "results_viewed" not in st.session_state:
    st.session_state.results_viewed = False
# Add this with your other session state initializations
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "file_names" not in st.session_state:
    st.session_state.file_names = []
# ---------------------------
# SIDEBAR RESET CONTROL
# ---------------------------
with st.sidebar:
    st.markdown("""
    <div style="
        font-size:1.4rem;
        font-weight:800;
        background: linear-gradient(90deg, #4AA3F0, #F5A623);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    ">🧭 Progress</div>
    """, unsafe_allow_html=True)

    current = st.session_state.current_page
    job_done = st.session_state.job_processed
    resumes_done = st.session_state.resumes_analyzed

    # Determine active step
    if current == "hero":
        active_step = 0
    elif current == "jd_upload" and not job_done:
        active_step = 1
    elif current == "jd_upload" and job_done and not resumes_done:
        active_step = 2
    elif current == "jd_upload" and resumes_done:
        active_step = 2
    elif current == "results" and not st.session_state.results_viewed:
        active_step = 3
    elif current == "results" and st.session_state.results_viewed and not st.session_state.csv_downloaded:
        active_step = 4
    elif current == "results" and st.session_state.csv_downloaded:
        active_step = 5
    else:
        active_step = 0

    step_labels = [
    ("0", "Get Started"),
    ("1", "Enter Job Description"),
    ("2", "Upload & Analyze Resumes"),
    ("3", "View Results"),
    ("4", "Analysis Complete")
    ]

    for i, (num, label) in enumerate(step_labels):
        step_num = int(num)

        if step_num < active_step:
            color = "#4AA3F0"
            glow = "0px 0px 8px rgba(74, 163, 240, 0.6)"
            opacity = "1"
            icon = "✓"
        elif step_num == active_step:
            color = "#F5A623"
            glow = "0px 0px 12px rgba(245, 166, 35, 0.8)"
            opacity = "1"
            icon = num
        else:
            color = "#444"
            glow = "none"
            opacity = "0.4"
            icon = num

        connector = ""
        if step_num < 4:
            connector_color = "#4AA3F0" if step_num < active_step else "#444"
            connector = f"<div style='width:2px; height:24px; background:{connector_color}; margin-left:15px; margin-bottom:8px; opacity:0.4;'></div>"

        st.markdown(f"""
        <div style="display:flex; align-items:center; margin-bottom:8px; opacity:{opacity};">
            <div style="
                min-width:32px;
                height:32px;
                border-radius:50%;
                border: 2px solid {color};
                box-shadow: {glow};
                display:flex;
                align-items:center;
                justify-content:center;
                color:{color};
                font-weight:700;
                font-size:0.9rem;
                margin-right:12px;
            ">{icon}</div>
            <div style="color:{color}; font-weight:600; font-size:0.95rem;">{label}</div>
        </div>
        {connector}
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 80px;'></div>", unsafe_allow_html=True)

    if st.button("🔄 Reset", key="reset_btn"):
        st.session_state.current_page = "hero"
        st.session_state.job_processed = False
        st.session_state.jd_text_saved = ""
        st.session_state.resumes_analyzed = False
        st.session_state.system = ResumeRankingSystem()
        st.session_state.uploaded_files = []  # Add this line
        st.session_state.file_names = []      # Add this line
        st.rerun()

# ---------------------------
# HERO PAGE
# ---------------------------
if st.session_state.current_page == "hero":
    
    st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, spacer, col2 = st.columns([1.2, 0.2, 1])

    with col1:
        st.markdown(f"""
        <div style="padding-top: 100px;">
            <div style="
                font-size:4rem;
                font-weight:800;
                background: linear-gradient(90deg, #4AA3F0, #F5A623);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                line-height:1.1;
            ">
                KAABIL-LENS
            </div>
            <div style="font-size:1.2rem; color:#636e72; margin-top:10px; margin-bottom:100px;">
                Transparent skill-based resume ranking with explainable scoring logic
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Get Started", key="get_started_btn"):
            st.session_state.current_page = "jd_upload"
            st.rerun()

    with col2:
       st.markdown('<div style="margin-top: -100px;">', unsafe_allow_html=True)
       if encoded_logo:
           st.image("static/image.png", use_container_width=True)
       st.markdown('</div>', unsafe_allow_html=True)
# ---------------------------
# JOB DESCRIPTION + RESUME PAGE
# ---------------------------
elif st.session_state.current_page == "jd_upload":

    # Step 1: Job Description Input
    st.markdown("""
    <div style="
        font-size:2.5rem;
        font-weight:800;
        background: linear-gradient(90deg, #4AA3F0, #F5A623);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    ">Job Description</div>
    """, unsafe_allow_html=True)  
    st.divider()

    st.markdown("""
    <div style="
        font-size:1.6rem;
        font-weight:700;
        color:#636e72;
        margin-bottom:12px;
    ">Paste the Job Description below</div>
    """, unsafe_allow_html=True)
    
    jd_text = st.text_area(
        "",
        value=st.session_state.jd_text_saved,
        height=220,
        disabled=st.session_state.job_processed
    )

    col1, col2 = st.columns([3.5, 1])
    jd_container = st.container()
    with jd_container:
     with col1:
        if not st.session_state.job_processed:
            if st.button("Analyze Job Description", key="analyze_jd_btn"):
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
            if st.button("Edit Job Description", key="edit_jd_btn"):
                st.session_state.job_processed = False
                st.session_state.system.job = None
                # Don't clear uploaded_files here!
                st.rerun()

    # Display Extracted Requirements
    if st.session_state.job_processed:
        job = st.session_state.system.job
        st.success("✅ Job Description processed successfully!")
        
        skills = job.skills if job.skills else []
        exp = job.required_experience
        
        skill_bullets = ""
        for skill in skills:
            skill_bullets += (
                '<div style="display:flex; align-items:center; gap:10px; margin-bottom:10px; color:#E0E0E0; font-size:1.3rem; font-weight:500;">'
                '<span style="width:13px; height:13px; border-radius:50%; border:2px solid #636e72; display:inline-block; flex-shrink:0;"></span>'
                f'{skill}'
                '</div>'
            )
        
        html = (
            '<div style="margin-top:16px; margin-bottom:16px;">'
            '<span style="font-size:1.6rem; font-weight:700; color:#4AA3F0;">Required Skills</span>'
            '</div>'
            '<div style="display:grid; grid-template-columns:1fr 1fr; gap:8px 40px; margin-top:10px;">'
            + skill_bullets +
            '</div>'
            '<div style="margin-top:24px; margin-bottom:8px;">'
            '<span style="font-size:1.6rem; font-weight:700; color:#F5A623;">Required Experience</span>'
            '</div>'
            f'<div style="color:#E0E0E0; font-size:1.3rem; font-weight:500; padding-left:4px;">{exp} years</div>'
        )
        
        st.markdown(html, unsafe_allow_html=True)
        # Step 2: Resume Upload
        # Step 2: Resume Upload
        st.divider()
        st.markdown("""
        <div style="
            font-size:2.5rem;
            font-weight:800;
            background: linear-gradient(90deg, #F5A623, #FDE68A);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        ">Resume Analysis</div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="
            font-size:1.6rem;
            font-weight:700;
            color:#636e72;
            margin-bottom:12px;
        ">Upload candidate resumes (PDF only)</div>
        """, unsafe_allow_html=True)
        
        # Modified file uploader to use session state
        uploaded_files = st.file_uploader(
            "",
            type=["pdf"],
            accept_multiple_files=True,
            key="resume_uploader"
        )
        
        # Update session state when files are uploaded
        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files
            st.session_state.file_names = [f.name for f in uploaded_files]
            st.session_state.resume_count = len(uploaded_files)  # Track count
        
        # Display files from session state (whether newly uploaded or from memory)
        if st.session_state.uploaded_files:
            file_bullets = ""
            for f in st.session_state.uploaded_files:
                file_bullets += (
                    '<div style="display:flex; align-items:center; gap:10px; margin-bottom:10px; color:#E0E0E0; font-size:1.1rem; font-weight:500;">'
                    '<span style="width:13px; height:13px; border-radius:50%; border:2px solid #636e72; display:inline-block; flex-shrink:0;"></span>'
                    f'{f.name}'
                    '</div>'
                )
            
            file_html = (
                f'<div style="margin-top:8px; margin-bottom:12px;">'
                f'<span style="font-size:1.3rem; font-weight:700; color:#4AA3F0;">{st.session_state.resume_count} file(s) uploaded</span>'  # Use count here
                f'</div>'
                f'<div style="margin-top:8px;">'
                + file_bullets +
                '</div>'
            )
            
            st.markdown(file_html, unsafe_allow_html=True)
            
            # Only show analyze button if resumes haven't been analyzed yet
            if not st.session_state.resumes_analyzed:
                if st.button("📊 Analyze Resumes", key="analyze_resumes_btn"):
                    st.session_state.system.resumes = []
        
                    with st.spinner("Processing resumes and scoring..."):
                        for file in st.session_state.uploaded_files:
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
                    st.rerun()

# ---------------------------
# BUTTON TO RESULTS PAGE
# ---------------------------
    if st.session_state.resumes_analyzed:
        st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="
            font-size:1.6rem;
            font-weight:700;
            color:#636e72;
            margin-bottom:12px;
        ">Ready to view results →</div>
        """, unsafe_allow_html=True)
        if st.button("➡️ Show Ranked Candidates", key="show_results_btn"):
            st.session_state.current_page = "results"
            st.rerun()
    
# ---------------------------
# RESULTS PAGE
# ---------------------------
elif st.session_state.current_page == "results":
    if not st.session_state.results_viewed:
        st.session_state.results_viewed = True
        st.rerun()

    # Final Results heading
    st.markdown("""
    <div style="padding-top: 10px;">
        <div style="
            font-size:4rem;
            font-weight:800;
            background: linear-gradient(90deg, #4AA3F0, #F5A623);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height:1.1;
        ">
            Final Results
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
     # Move this outside

    if not st.session_state.system.resumes:
        st.warning("No resumes available. Go back and upload resumes first.")
    else:
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

        st.markdown("""
        <div style="
            font-size:2.6rem;
            font-weight:1000;
            color:#F5A623;
            margin-top:24px;
            margin-bottom:12px;
        ">Analytics</div>
        """, unsafe_allow_html=True)
        
        st.dataframe(
            df[["Rank", "Candidate", "Skill Match (%)", "Experience Match (%)", "Final Score"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank": st.column_config.NumberColumn("Rank", width="small"),
                "Candidate": st.column_config.TextColumn("Candidate", width="medium"),
                "Skill Match (%)": st.column_config.ProgressColumn(
                    "Skill Match",
                    min_value=0,
                    max_value=100,
                    format="%d%%"
                ),
                "Experience Match (%)": st.column_config.ProgressColumn(
                    "Experience Match",
                    min_value=0,
                    max_value=100,
                    format="%d%%"
                ),
                "Final Score": st.column_config.ProgressColumn(
                    "Final Score",
                    min_value=0,
                    max_value=100,
                    format="%.1f"
                ),
            }
        )
        
        st.divider()
        
        st.markdown("""
        <div style="
            font-size:2.6rem;
            font-weight:1000;
            color:#4AA3F0;
            margin-top:24px;
            margin-bottom:12px;
        ">Skill Gap Report</div>
        """, unsafe_allow_html=True)
        
        for i, r in enumerate(st.session_state.system.resumes, start=1):
            with st.expander(f"{i}. {r.name}"):
                matched = r.matched_skills if r.matched_skills else []
                missing = r.missing_skills if r.missing_skills else []
        
                matched_bullets = "".join(
                    '<div style="display:flex; align-items:center; gap:8px; margin-bottom:8px; color:#E0E0E0; font-size:1rem;">'
                    '<span style="width:10px; height:10px; border-radius:50%; border:2px solid #00b894; display:inline-block; flex-shrink:0;"></span>'
                    f'{skill}'
                    '</div>'
                    for skill in matched
                ) if matched else '<div style="color:#636e72; font-size:1rem;">None</div>'
        
                missing_bullets = "".join(
                    '<div style="display:flex; align-items:center; gap:8px; margin-bottom:8px; color:#E0E0E0; font-size:1rem;">'
                    '<span style="width:10px; height:10px; border-radius:50%; border:2px solid #ff4b4b; display:inline-block; flex-shrink:0;"></span>'
                    f'{skill}'
                    '</div>'
                    for skill in missing
                ) if missing else '<div style="color:#636e72; font-size:1rem;">None</div>'
        
                st.markdown(
                    '<div style="font-size:1.1rem; font-weight:700; color:#00b894; margin-bottom:8px;">Matched Skills</div>'
                    + matched_bullets +
                    '<div style="font-size:1.1rem; font-weight:700; color:#ff4b4b; margin-top:16px; margin-bottom:8px;">Missing Skills</div>'
                    + missing_bullets,
                    unsafe_allow_html=True
                )

        csv = df.to_csv(index=False)
        col1, col2 = st.columns([1.85, 1])
        with col1:
            if st.button("⬅️ Back to Job/Resume Page", key="back_btn"):
                st.session_state.current_page = "jd_upload"
                st.session_state.results_viewed = False
                st.session_state.csv_downloaded = False
                st.rerun()
        with col2:
            if st.download_button(
                label="📥 Download CSV of Ranked Candidates",
                data=csv,
                file_name="ranked_candidates.csv",
                mime="text/csv",
                key="download_btn"
            ):
                st.session_state.csv_downloaded = True
                st.rerun()