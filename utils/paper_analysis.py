import os
import re
import json
import google.generativeai as genai
import PyPDF2
import streamlit as st
from dotenv import load_dotenv
from collections import Counter

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

# ---------------- KEYWORD ANALYSIS ----------------
def get_top_keywords(text, top_n=30):
    """Return top N most common words (filtering stopwords)."""
    stopwords = set("""
    the is in at of and a to for with on as by an be this that from or are it
    """.split())
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9-]+\b", text.lower())
    words = [w for w in words if w not in stopwords and len(w) > 2]
    freq = Counter(words)
    return [word for word, _ in freq.most_common(top_n)]

# ---------------- MAIN TOPIC EXTRACTION ----------------
def predict_topics_from_papers(combined_text, num_topics=10):
    """
    Extracts keywords locally, then sends them to Gemini in ONE call
    for detailed topic importance analysis.
    """
    st.info("🔍 Analyzing question papers… please wait.")

    # Get top keywords locally
    keywords = get_top_keywords(combined_text, top_n=40)

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        You are analyzing exam question papers.

        Based on these keywords:
        {', '.join(keywords)}

        Identify the top {num_topics} exam topics.
        For each topic, provide:
        - topic: clear name
        - importance: integer 0–100 (percentage)
        - details: 1–2 sentence description of why it's important.

        Return the output as a JSON list like:
        [
          {{"topic": "Topic Name", "importance": 85, "details": "Reason here"}},
          ...
        ]
        """

        response = model.generate_content(prompt, request_options={"timeout": 60})
        raw_text = getattr(response, "text", "").strip()

        topics = json.loads(raw_text)
        topics.sort(key=lambda x: x["importance"], reverse=True)
        return topics

    except Exception as e:
        return [{"topic": f"Error: {e}", "importance": 0, "details": ""}]
