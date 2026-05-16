import streamlit as st
import pdfplumber
import os
import json
from openai import OpenAI

# PAGE CONFIG
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="👜",
    layout="wide"
)

# OPENAI API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# CUSTOM CSS
st.markdown("""
<style>

/* ---------- MAIN ---------- */
.stApp {
    background: linear-gradient(to right, #f8fafc, #eef2ff);
    font-family: 'Segoe UI', sans-serif;
}

/* ---------- TITLE ---------- */
.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #64748b;
    font-size: 18px;
    margin-bottom: 30px;
}

/* ---------- METRICS ---------- */
[data-testid="metric-container"] {
    background: white;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
    border-left: 6px solid #14b8a6;
}

/* ---------- BUTTON ---------- */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #7c3aed, #8b5cf6);
    color: white;
    border: none;
    padding: 14px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: bold;
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(90deg, #6d28d9, #7c3aed);
}

/* ---------- PROGRESS BAR ---------- */
.stProgress > div > div > div > div {
    background-color: #f59e0b;
}

/* ---------- GENERAL CARD ---------- */
.card {
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    transition: 0.3s ease;
}

.card:hover {
    transform: translateY(-2px);
}

/* ---------- SUMMARY ---------- */
.summary-card {
    background: #dbeafe;
    border-left: 6px solid #2563eb;
    color: #1e3a8a;
}

/* ---------- STRENGTH ---------- */
.strength-card {
    background: #ccfbf1;
    border-left: 6px solid #14b8a6;
    color: #134e4a;
}

/* ---------- WEAKNESS ---------- */
.weakness-card {
    background: #ffe7d6;
    border-left: 6px solid #f97316;
    color: #9a3412;
}

/* ---------- SUGGESTIONS ---------- */
.suggestion-card {
    background: #f3e8ff;
    border-left: 6px solid #9333ea;
    color: #581c87;
}

/* ---------- SKILLS ---------- */
.skill-tag {
    background: linear-gradient(90deg, #7c3aed, #8b5cf6);
    color: white;
    padding: 8px 16px;
    border-radius: 30px;
    margin: 5px;
    display: inline-block;
    font-size: 14px;
    font-weight: 600;
}

/* ---------- WORD COUNT ---------- */
.word-box {
    background: #fef3c7;
    color: #92400e;
    padding: 14px;
    border-radius: 14px;
    margin-top: 10px;
    border-left: 6px solid #f59e0b;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown(
    "<div class='main-title'>AI Resume Analyzer 💼</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Smart AI-powered resume insights and career feedback</div>",
    unsafe_allow_html=True
)

# FILE UPLOAD
uploaded_file = st.file_uploader(
    "📄 Upload Your Resume (PDF)",
    type=["pdf"]
)

# TEXT EXTRACTION
def extract_text(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text


# SKILL DETECTION
skills_list = [
    "python",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "sql",
    "data analysis",
    "java",
    "c++",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "git",
    "docker"
]

def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills


# AI ANALYSIS
def ai_analysis(text):

    response = client.chat.completions.create(
        model="gpt-4o-mini",

        messages=[
            {
                "role": "system",
                "content": """
You are a professional resume reviewer and career mentor.

Analyze the resume in a friendly and human tone.

Return ONLY valid JSON in this format:

{
  "summary": "...",
  "strengths": ["...", "..."],
  "weaknesses": ["...", "..."],
  "suggestions": ["...", "..."]
}

Guidelines:
- Sound supportive and professional
- Give practical career advice
- Keep language simple and clear
- Avoid robotic wording
"""
            },

            {
                "role": "user",
                "content": f"Resume:\n{text[:4000]}"
            }
        ]
    )

    return response.choices[0].message.content


# MAIN LOGIC
if uploaded_file:

    st.success("✅ Resume Uploaded Successfully")

    # Extract text
    text = extract_text(uploaded_file)

    # Skills
    skills = extract_skills(text)

    # Score calculation
    score = min(len(skills) * 10, 100)

    # Word count
    word_count = len(text.split())

  
    # DASHBOARD
  
    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Skills Detected", len(skills))
    col2.metric("Resume Score", f"{score}/100")
    col3.metric("Word Count", word_count)

    st.progress(score)

  
    # SCORE MESSAGE
  
    if score >= 80:
        st.success("🔥 Excellent Resume")
    elif score >= 50:
        st.warning("👍 Good Resume — can improve more")
    else:
        st.error("⚠️ Resume needs improvement")

  
    # WORD COUNT BOX
  
    st.markdown(
        f"<div class='word-box'>📄 Resume Word Count: {word_count}</div>",
        unsafe_allow_html=True
    )

  
    # SKILLS SECTION
  
    st.subheader("🧠 Skills & Technologies")

    if skills:
        for skill in skills:
            st.markdown(
                f"<span class='skill-tag'>{skill}</span>",
                unsafe_allow_html=True
            )
    else:
        st.info("No major skills detected")

    st.write("")

   
    # AI ANALYSIS BUTTON
    
    st.subheader("🤖 AI Career Feedback")

    if st.button("Generate AI Analysis"):

        with st.spinner("🤖 AI is analyzing your resume..."):

            result = ai_analysis(text)

            try:
                data = json.loads(result)

                #  SUMMARY 
                st.subheader("📌 Professional Summary")

                st.markdown(
                    f"""
                    <div class='card summary-card'>
                    {data['summary']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                #  STRENGTHS 
                st.subheader("💪 Key Strengths")

                for strength in data["strengths"]:

                    st.markdown(
                        f"""
                        <div class='card strength-card'>
                        ✅ {strength}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # WEAKNESSES 
                st.subheader("⚠️ Areas to Improve")

                for weakness in data["weaknesses"]:

                    st.markdown(
                        f"""
                        <div class='card weakness-card'>
                        ❌ {weakness}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                #  SUGGESTIONS 
                st.subheader("💡 Career Suggestions")

                for suggestion in data["suggestions"]:

                    st.markdown(
                        f"""
                        <div class='card suggestion-card'>
                        🚀 {suggestion}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            except Exception as e:

                st.error("Error reading AI response")
                st.write(result)

else:

    st.info("👆 Upload a PDF resume to start analysis")