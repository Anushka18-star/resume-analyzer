import streamlit as st
import pdfplumber
import re

# -------------------------------
# UI Styling (Light Theme)
# -------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fb;
    }
    .block-container {
        padding-top: 2rem;
    }
    h1 {
        text-align: center;
        color: #2c3e50;
    }
    p {
        text-align: center;
        color: gray;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------
st.markdown("<h1>AI Resume Analyzer 💼</h1>", unsafe_allow_html=True)
st.markdown("<p>Analyze your resume like an ATS system</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📄 Upload your resume (PDF)", type=["pdf"])

# -------------------------------
# Extract text from PDF
# -------------------------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# -------------------------------
# Extract skills
# -------------------------------
def extract_skills(text, skills_list):
    text = text.lower()
    found_skills = []
    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)
    return found_skills

# -------------------------------
# Generate summary
# -------------------------------
def generate_summary(text):
    text = text.replace("\n", " ")
    sentences = re.split(r'(?<=[.!?]) +', text)
    filtered = [s for s in sentences if len(s.split()) > 6]
    return " ".join(filtered[:3])

# -------------------------------
# Job match score
# -------------------------------
def match_score(resume_text, job_desc):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_desc.lower().split())
    if len(job_words) == 0:
        return 0
    match = resume_words.intersection(job_words)
    return round((len(match) / len(job_words)) * 100, 2)

# -------------------------------
# Skills list
# -------------------------------
skills_list = [
    "python", "machine learning", "data analysis",
    "sql", "tensorflow", "deep learning",
    "java", "c++", "html", "css", "javascript"
]

# -------------------------------
# MAIN APP
# -------------------------------
if uploaded_file:
    st.success("✅ Resume uploaded successfully!")

    text = extract_text_from_pdf(uploaded_file)

    # Summary
    st.divider()
    st.subheader("📌 Professional Summary")
    summary = generate_summary(text)
    st.write(summary if summary else "Summary not found")

    # Skills
    skills = extract_skills(text, skills_list)

    # Job Description
    job_desc = st.text_area("📌 Paste Job Description")

    job_match = 0
    if job_desc:
        job_match = match_score(text, job_desc)

    # Resume Score
    resume_score = min(len(skills) * 10, 100)

    # Dashboard
    st.divider()
    st.subheader("📊 Analysis Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Skills Found", len(skills))
    col2.metric("Resume Score", f"{resume_score}/100")
    col3.metric("Job Match", f"{job_match}%")

    # Progress
    st.divider()
    st.subheader("📈 Scores")

    st.write("Resume Score")
    st.progress(resume_score)

    if job_desc:
        st.write("Job Match Score")
        st.progress(int(job_match))

    # Skills display
    st.divider()
    st.subheader("🧠 Extracted Skills")
    st.write(skills if skills else "No skills found")

    # Suggestions
    st.divider()
    st.subheader("💡 Suggestions")

    missing_skills = [skill for skill in skills_list if skill not in skills]

    if missing_skills:
        st.write("Consider adding these skills:")
        st.write(missing_skills[:5])

    if resume_score < 50:
        st.warning("Add more technical skills and projects")
    elif resume_score < 80:
        st.info("Good resume, but can be improved")
    else:
        st.success("Great resume! 🎉")

    # Download report
    report = f"""
    Resume Analysis Report

    Skills Found: {skills}
    Resume Score: {resume_score}/100
    Job Match Score: {job_match}%

    Suggestions:
    - Improve missing skills
    - Add more projects
    """

    st.download_button("📄 Download Report", report, file_name="resume_report.txt")

else:
    st.info("👆 Upload a resume to get started")