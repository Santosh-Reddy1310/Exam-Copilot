import os
import re
import google.generativeai as genai
import PyPDF2
import streamlit as st
from dotenv import load_dotenv
from collections import defaultdict

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
    # Clean up excessive whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ---------------- HELPER: CHUNKING ----------------
def chunk_text(text, chunk_size=3000):
    """Split long text into smaller chunks."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# ---------------- MAIN TOPIC EXTRACTION ----------------
def predict_topics_from_papers(combined_text, num_topics=10):
    """
    Splits PDF text into chunks, processes each with Gemini,
    and merges results with importance percentages.
    """
    chunks = chunk_text(combined_text, chunk_size=3000)
    total_chunks = len(chunks)
    topic_scores = defaultdict(list)
    topic_details = defaultdict(str)

    # Process each chunk with a progress bar
    progress_bar = st.progress(0)
    for idx, chunk in enumerate(chunks, start=1):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""
            From the following exam questions text, extract the top {num_topics} most important topics.
            For each topic, give:
            - Topic name
            - Estimated importance (0–100) based on frequency/relevance
            - Short 1–2 sentence detail

            Return in JSON list format like:
            [
              {{"topic": "...", "importance": 85, "details": "..."}},
              ...
            ]

            Exam Questions:
            {chunk}
            """

            response = model.generate_content(prompt, request_options={"timeout": 60})
            raw_text = getattr(response, "text", "").strip()

            import json
            topics = json.loads(raw_text)

            # Merge topics across chunks
            for t in topics:
                name = t["topic"].strip()
                topic_scores[name].append(t["importance"])
                if not topic_details[name]:
                    topic_details[name] = t["details"]

        except Exception as e:
            st.warning(f"Error processing chunk {idx}/{total_chunks}: {e}")

        progress_bar.progress(idx / total_chunks)

    # Average importance scores & sort
    merged_results = [
        {
            "topic": name,
            "importance": round(sum(scores) / len(scores), 2),
            "details": topic_details[name]
        }
        for name, scores in topic_scores.items()
    ]
    merged_results.sort(key=lambda x: x["importance"], reverse=True)

    return merged_results[:num_topics]
