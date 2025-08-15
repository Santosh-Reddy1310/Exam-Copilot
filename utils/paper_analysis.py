import os
import re
import json
import time
import PyPDF2
import streamlit as st
from dotenv import load_dotenv
from collections import Counter
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF file."""
    text = ""
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    # Clean whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ---------------- LOCAL KEYWORD ANALYSIS ----------------
def local_topic_analysis(text, num_topics=10):
    """Local fallback if AI call fails."""
    stopwords = set("""
    the is in at of and a to for with on as by an be this that from or are it
    """.split())
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9-]+\b", text.lower())
    words = [w for w in words if w not in stopwords and len(w) > 2]
    freq = Counter(words)
    top_words = [word for word, _ in freq.most_common(num_topics)]
    return [{"topic": w, "importance": 50, "details": "Keyword extracted locally."} for w in top_words]

# ---------------- MAIN TOPIC EXTRACTION ----------------
def predict_topics_from_papers(combined_text, num_topics=10):
    """Tries Gemini AI for topics, falls back to local if timeout/fail."""
    st.info("🔍 Analyzing question papers… please wait.")

    # Truncate to safe size
    if len(combined_text) > 15000:
        combined_text = combined_text[:15000]

    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"""
        You are analyzing exam question papers.

        From the following text, extract the top {num_topics} exam topics.
        For each topic, provide:
        - topic: clear name
        - importance: integer 0–100 (percentage)
        - details: 1–2 sentence description.

        Return ONLY valid JSON list:
        [
          {{"topic": "Topic Name", "importance": 85, "details": "Reason here"}},
          ...
        ]

        Exam Questions:
        {combined_text}
        """

        start_time = time.time()
        response = model.generate_content(prompt, request_options={"timeout": 10})
        elapsed = time.time() - start_time

        if elapsed > 10:
            st.warning("⚠ Gemini API is slow. Using offline analysis.")
            return local_topic_analysis(combined_text, num_topics)

        raw_text = getattr(response, "text", "").strip()
        topics = json.loads(raw_text)
        topics.sort(key=lambda x: x["importance"], reverse=True)
        return topics

    except Exception as e:
        st.warning(f"⚠ AI request failed: {e}")
        return local_topic_analysis(combined_text, num_topics)
