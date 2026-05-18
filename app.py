# =========================================================
# AI Resume Screening System
# Premium Streamlit Version
# app.py
# =========================================================

import streamlit as st
import streamlit.components.v1 as components
import os
import re
import nltk
import PyPDF2

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)

# =========================================================
# NLTK DOWNLOAD
# =========================================================

nltk.download("stopwords")

stop_words = set(stopwords.words("english"))

# =========================================================
# CREATE RESUME FOLDER
# =========================================================

UPLOAD_FOLDER = "resumes"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background:
    radial-gradient(circle at top,#0f172a,#020617);
    color:white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.title {
    text-align:center;
    font-size:64px;
    font-weight:800;
    margin-bottom:10px;

    background: linear-gradient(
        to right,
        #38bdf8,
        #3b82f6,
        #c084fc
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.subtitle {
    text-align:center;
    color:#cbd5e1;
    font-size:24px;
    margin-bottom:50px;
}

.section-title {
    font-size:28px;
    font-weight:700;
    margin-bottom:15px;
    color:white;
}

textarea {
    font-size:18px !important;
}

.stButton > button {
    height:60px;
    border-radius:14px;
    background:linear-gradient(to right,#2563eb,#7c3aed);
    color:white;
    font-size:20px;
    font-weight:700;
    border:none;
}

.stButton > button:hover {
    opacity:0.9;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.markdown("""
<div class="title">
    AI Resume Screening System
</div>

<div class="subtitle">
    Smart Candidate Ranking 
</div>
""", unsafe_allow_html=True)

# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_text_from_pdf(pdf_path):

    text = ""

    with open(pdf_path, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text

# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z ]",
        " ",
        text
    )

    words = text.split()

    words = [
        word for word in words
        if word not in stop_words
    ]

    return " ".join(words)

# =========================================================
# MATCH RESUMES
# =========================================================

def match_resumes(job_description, resumes):

    documents = [job_description] + resumes

    tfidf = TfidfVectorizer()

    matrix = tfidf.fit_transform(documents)

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:]
    )

    return similarity[0]

# =========================================================
# LAYOUT
# =========================================================

col1, col2 = st.columns(2)

# =========================================================
# JOB DESCRIPTION
# =========================================================

with col1:

    st.markdown(
        '<div class="section-title">📄 Paste Job Description</div>',
        unsafe_allow_html=True
    )

    job_description = st.text_area(
        "",
        height=320,
        placeholder="""
Example Skills:

- Python
- Machine Learning
- NLP
- SQL
- Flask / Streamlit
- Deep Learning
- Problem Solving
        """
    )

# =========================================================
# RESUME UPLOAD
# =========================================================

with col2:

    st.markdown(
        '<div class="section-title">☁ Upload Resume PDFs</div>',
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "",
        type=["pdf"],
        accept_multiple_files=True
    )

# =========================================================
# SCREEN BUTTON
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

screen = st.button(
    "🔍 Screen Resumes",
    use_container_width=True
)

# =========================================================
# PROCESSING
# =========================================================

if screen:

    # =====================================================
    # VALIDATIONS
    # =====================================================

    if not job_description:

        st.error("Please enter Job Description.")

    elif not uploaded_files:

        st.error("Please upload resumes.")

    else:

        resume_texts = []

        names = []

        # =================================================
        # SAVE + EXTRACT TEXT
        # =================================================

        with st.spinner("Analyzing resumes..."):

            for file in uploaded_files:

                filepath = os.path.join(
                    UPLOAD_FOLDER,
                    file.name
                )

                with open(filepath, "wb") as f:
                    f.write(file.getbuffer())

                extracted_text = extract_text_from_pdf(
                    filepath
                )

                cleaned_resume = clean_text(
                    extracted_text
                )

                resume_texts.append(
                    cleaned_resume
                )

                names.append(
                    file.name
                )

        # =================================================
        # CLEAN JOB DESCRIPTION
        # =================================================

        cleaned_jd = clean_text(
            job_description
        )

        # =================================================
        # MATCHING
        # =================================================

        scores = match_resumes(
            cleaned_jd,
            resume_texts
        )

        results = list(
            zip(names, scores)
        )

        results.sort(
            key=lambda x: x[1],
            reverse=True
        )

        # =================================================
        # RESULTS
        # =================================================

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">🏆 Top Candidates</div>',
            unsafe_allow_html=True
        )

        for rank, (name, score) in enumerate(results, start=1):

            percentage = round(score * 100, 2)

            components.html(
                f"""
                <div style="
                    background:#111827;
                    padding:25px;
                    border-radius:20px;
                    margin-bottom:20px;
                    border:1px solid rgba(255,255,255,0.08);
                    box-shadow:0 4px 20px rgba(0,0,0,0.3);
                    color:white;
                    font-family:Arial;
                ">

                    <div style="
                        color:#94a3b8;
                        font-size:16px;
                        margin-bottom:10px;
                    ">
                        Rank #{rank}
                    </div>

                    <div style="
                        font-size:24px;
                        font-weight:600;
                        margin-bottom:12px;
                    ">
                        {name}
                    </div>

                    <div style="
                        color:#22c55e;
                        font-size:42px;
                        font-weight:700;
                    ">
                        {percentage}%
                    </div>

                </div>
                """,
                height=180
            )

            st.progress(float(score))

        # =================================================
        # BEST MATCH
        # =================================================

        best_candidate = results[0]

        st.success(
            f"🏆 Best Match: {best_candidate[0]} "
            f"with score {round(best_candidate[1]*100,2)}%"
        )