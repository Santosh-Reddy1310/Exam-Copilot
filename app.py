import streamlit as st
import pandas as pd
from utils.paper_analysis import extract_text_from_pdf, predict_topics_from_papers
from utils.study_planner import stress_test_plan
from utils.clarity_bot import explain_in_levels

# --- Page Config ---
st.set_page_config(
    page_title="Exam Copilot 📝",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Monochromatic Black & White Theme ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global black theme */
.stApp {
    background-color: #000000;
    color: #ffffff;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Remove default streamlit padding */
.main > div {
    padding-top: 2rem;
}

/* Header styling */
h1 {
    color: #ffffff;
    font-weight: 700;
    font-size: 2.5rem;
    text-align: center;
    margin-bottom: 0.5rem;
}

h2, h3, h4 {
    color: #ffffff;
    font-weight: 600;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #000000;
    border-radius: 12px;
    padding: 8px;
    margin-bottom: 2rem;
    border: 1px solid #ffffff;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    border-radius: 8px;
    color: #ffffff;
    font-weight: 500;
    padding: 12px 24px;
    transition: all 0.3s ease;
    border: 1px solid transparent;
}

.stTabs [aria-selected="true"] {
    background-color: #ffffff;
    color: #000000 !important;
    font-weight: 600;
    border: 1px solid #ffffff;
}

/* Enhanced card style */
.card {
    background-color: #000000;
    padding: 2rem;
    border-radius: 16px;
    border: 2px solid #ffffff;
    margin: 1rem 0 2rem 0;
    position: relative;
    max-width: 100%;
    width: 100%;
}

/* Section headers */
.card h3 {
    color: #ffffff;
    font-weight: 600;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Button container for spacing */
.stButton {
    margin: 1.5rem 0 !important;
    width: 100%;
}

/* Enhanced buttons */
.stButton > button {
    background-color: #ffffff;
    color: #000000;
    border-radius: 8px;
    border: 2px solid #ffffff;
    padding: 0.75rem 2rem;
    font-weight: 600;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    text-transform: none;
    letter-spacing: 0.025em;
    width: 100%;
    margin: 0 auto;
    display: block;
}

.stButton > button:hover {
    background-color: #000000;
    color: #ffffff;
    border: 2px solid #ffffff;
    transform: translateY(-2px);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Input fields */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div {
    background-color: #000000 !important;
    border: 2px solid #ffffff !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    padding: 12px 16px !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus {
    border-color: #ffffff !important;
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.3) !important;
    outline: none !important;
}

/* Fix for text area height */
.stTextArea > div > div > textarea {
    min-height: 150px !important;
    resize: vertical !important;
}

/* Fix selectbox alignment */
.stSelectbox > div {
    width: 100% !important;
}

.stSelectbox > div > div {
    width: 100% !important;
}

/* File uploader */
.stFileUploader > div {
    background-color: #000000;
    border: 2px dashed #ffffff;
    border-radius: 12px;
    padding: 2rem;
    transition: all 0.3s ease;
    text-align: center;
    width: 100%;
}

.stFileUploader > div:hover {
    border-color: #ffffff;
    background-color: rgba(255, 255, 255, 0.1);
}

/* Column spacing for form elements */
.stColumns > div {
    padding: 0 0.5rem;
}

.stColumns {
    gap: 1rem;
    width: 100%;
}

/* Form element spacing */
.stTextInput, .stTextArea, .stNumberInput, .stSelectbox, .stSlider {
    margin-bottom: 1rem !important;
}

/* Fix slider styling */
.stSlider {
    padding: 1rem 0;
}

.stSlider > div > div > div > div {
    background-color: #ffffff !important;
}

.stSlider > div > div > div {
    background-color: #ffffff !important;
    opacity: 0.3;
}

/* Center content properly */
.main .block-container {
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100%;
}

/* Tab container improvements */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #000000;
    border-radius: 12px;
    padding: 8px;
    margin: 1rem 0 2rem 0;
    border: 1px solid #ffffff;
    width: 100%;
    justify-content: center;
}

/* Enhanced tables */
.stDataFrame > div {
    background-color: #000000;
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid #ffffff;
}

table {
    border-collapse: collapse;
    width: 100%;
    font-size: 0.9rem;
}

thead th {
    background-color: #ffffff;
    color: #000000;
    font-weight: 600;
    padding: 1rem;
    text-align: left;
    border-bottom: 2px solid #ffffff;
}

tbody td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #ffffff;
    color: #ffffff;
}

tbody tr:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

/* Labels */
.stTextInput > label,
.stTextArea > label,
.stNumberInput > label,
.stSelectbox > label,
.stSlider > label {
    color: #ffffff !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    margin-bottom: 0.5rem !important;
}

/* Success/Warning messages */
.stSuccess > div {
    background-color: #000000;
    border: 2px solid #ffffff;
    border-radius: 8px;
    color: #ffffff;
}

.stWarning > div {
    background-color: #000000;
    border: 2px solid #ffffff;
    border-radius: 8px;
    color: #ffffff;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #ffffff !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #000000;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: #ffffff;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #ffffff;
    opacity: 0.8;
}

/* Additional button spacing */
.stButton + .stButton {
    margin-top: 1.5rem !important;
}

/* Number input styling fixes */
.stNumberInput input[type=number] {
    -moz-appearance: textfield;
}

.stNumberInput input[type=number]::-webkit-outer-spin-button,
.stNumberInput input[type=number]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

/* Placeholder text styling */
::placeholder {
    color: rgba(255, 255, 255, 0.5) !important;
    opacity: 1 !important;
}

/* Help text styling */
.help {
    color: rgba(255, 255, 255, 0.7) !important;
    font-size: 0.85rem !important;
}

/* Ensure proper width for all form elements */
.element-container {
    width: 100% !important;
}

.stForm {
    width: 100%;
}

/* Fix any overflow issues */
.stApp > div {
    overflow-x: hidden;
}

/* Responsive design */
@media (max-width: 768px) {
    .card {
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    h1 {
        font-size: 2rem;
    }
    
    .stButton > button {
        padding: 0.6rem 1.5rem;
        font-size: 0.9rem;
    }
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1>Exam Copilot 📝</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ffffff; font-size: 1.1rem; margin-bottom: 3rem;'>Your AI-powered study companion for exam preparation</p>", unsafe_allow_html=True)

# --- Session State ---
if 'study_plan_output' not in st.session_state:
    st.session_state['study_plan_output'] = ""
if 'clarity_bot_output' not in st.session_state:
    st.session_state['clarity_bot_output'] = ""

# --- Tabs ---
tabs = st.tabs(["📚 Paper Analysis", "🗓️ Study Planner", "💡 Clarity Bot"])

# =========================
# Paper Analysis Tab
# =========================
with tabs[0]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📚 Paper Analysis: Important Topics from Question Papers")
    st.markdown("<p style='color: #ffffff; margin-bottom: 1.5rem;'>Upload your question papers and let AI identify the most important topics for your preparation.</p>", unsafe_allow_html=True)

    uploaded_pdfs = st.file_uploader(
        "Upload one or more PDF question papers",
        type=["pdf"],
        accept_multiple_files=True,
        help="Select multiple PDF files containing past question papers"
    )

    num_topics = st.slider("Number of important topics to extract:", 1, 20, 10)

    if st.button("Extract Important Topics", key="extract_topics"):
        if uploaded_pdfs:
            combined_text = ""
            for pdf_file in uploaded_pdfs:
                combined_text += extract_text_from_pdf(pdf_file) + "\n"

            with st.spinner("Analyzing and extracting topics..."):
                topics_data = predict_topics_from_papers(combined_text, num_topics=num_topics)

            st.success("Topics extracted successfully!")

            # Display in table format
            if isinstance(topics_data, list) and topics_data and "topic" in topics_data[0]:
                df = pd.DataFrame(topics_data)
                df = df[["topic", "importance", "details"]]  # Keep consistent column order
                df.columns = ["Topic", "Importance (%)", "Details"]
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No valid topics found. Check your PDF content or API output.")
        else:
            st.warning("Please upload at least one PDF file.")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Study Planner Tab
# =========================
with tabs[1]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🗓️ Study Planner: Create a Stress-Test Study Plan")
    st.markdown("<p style='color: #9ca3af; margin-bottom: 1.5rem;'>Generate a comprehensive study schedule optimized for your exam timeline and daily study capacity.</p>", unsafe_allow_html=True)
    
    study_topics = st.text_area("Enter topics for your study plan (one per line):", height=150, 
                               placeholder="Enter each topic on a new line...\nExample:\n- Data Structures\n- Algorithms\n- Database Management")
    
    col1, col2 = st.columns(2)
    with col1:
        study_duration = st.number_input("Study duration in days:", min_value=1, max_value=365, value=7)
    with col2:
        hours_per_day = st.number_input("Hours per day:", min_value=1, max_value=24, value=6)

    if st.button("Generate Study Plan", key="generate_plan"):
        if study_topics:
            topics_list = [t.strip() for t in study_topics.split("\n") if t.strip()]
            with st.spinner("Generating study plan..."):
                plan = stress_test_plan(topics_list, hours_per_day=hours_per_day, days_until_exam=study_duration)
                st.session_state['study_plan_output'] = plan
            st.success("Study Plan Ready!")
            st.markdown(st.session_state['study_plan_output'])
        else:
            st.warning("Please enter some topics.")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Clarity Bot Tab
# =========================
with tabs[2]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 💡 Clarity Bot: Explain Concepts in Multiple Levels")
    st.markdown("<p style='color: #9ca3af; margin-bottom: 1.5rem;'>Get clear, level-appropriate explanations for any concept to enhance your understanding.</p>", unsafe_allow_html=True)
    
    concept_to_explain = st.text_input("Enter the concept you want explained:", 
                                      placeholder="e.g., Machine Learning, Photosynthesis, Quantum Physics...")
    
    explanation_level = st.selectbox("Select explanation level:", 
                                     ["Beginner", "Intermediate", "Advanced", "Expert"],
                                     help="Choose the complexity level that matches your current understanding")

    if st.button("Get Explanation", key="get_explanation"):
        if concept_to_explain:
            with st.spinner("Getting explanation..."):
                explanation = explain_in_levels(concept_to_explain, level=explanation_level)
                st.session_state['clarity_bot_output'] = explanation
            st.success("Explanation Ready!")
            st.markdown(st.session_state['clarity_bot_output'])
        else:
            st.warning("Please enter a concept.")
    st.markdown("</div>", unsafe_allow_html=True)