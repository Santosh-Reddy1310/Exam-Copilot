import streamlit as st
from utils.paper_analysis import extract_text_from_pdf, predict_topics_from_papers
from utils.study_planner import stress_test_plan
from utils.clarity_bot import explain_in_levels

st.set_page_config(page_title="📚 Exam Copilot", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    body { background-color: black; color: white; }
    table { color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Exam Copilot")

tabs = st.tabs(["📄 Paper Analysis", "🗓 Study Planner", "💡 Clarity Bot"])

# ---------------- PAPER ANALYSIS ----------------
with tabs[0]:
    st.subheader("📄 Analyze Past Papers")
    uploaded_pdfs = st.file_uploader(
        "Upload one or more PDF question papers",
        type=["pdf"], accept_multiple_files=True
    )

    if uploaded_pdfs:
        combined_text = ""
        for pdf in uploaded_pdfs:
            combined_text += extract_text_from_pdf(pdf) + "\n"

        if st.button("Analyze Papers"):
            topics = predict_topics_from_papers(combined_text)
            st.subheader("📌 Important Topics")
            st.table(topics)

# ---------------- STUDY PLANNER ----------------
with tabs[1]:
    st.subheader("🗓 Create a Study Plan")
    days_until_exam = st.number_input("Days until exam", min_value=1, value=7)
    daily_hours = st.number_input("Daily study hours", min_value=1, value=6)
    intensity = st.selectbox("Intensity", ["Low", "Moderate", "High"])
    break_frequency = st.text_input("Break frequency", "Every 45 mins")
    subjects = st.text_area("Subjects (comma separated)", "Java, Probability & Statistics, Operating Systems, Digital Logic")

    if st.button("Generate Plan"):
        topics = [s.strip() for s in subjects.split(",") if s.strip()]
        plan = stress_test_plan(days_until_exam, daily_hours, intensity, break_frequency, topics)
        st.subheader("📅 Study Timetable")
        st.markdown(plan)

# ---------------- CLARITY BOT ----------------
with tabs[2]:
    st.subheader("💡 Explain a Concept")
    concept = st.text_input("Enter a concept")
    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced", "Expert"])
    context = st.text_area("Context (optional)")

    if st.button("Explain"):
        explanation = explain_in_levels(concept, level, {"context": context})
        st.markdown(explanation)
