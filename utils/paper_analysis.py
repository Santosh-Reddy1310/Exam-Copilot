import PyPDF2
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_pdf(file):
    """
    Extract text from a PDF file with error handling.
    """
    text = ""
    try:
        reader = PyPDF2.PdfReader(file)
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page_text + "\n"
            except Exception as e:
                print(f"Warning: Could not extract text from page {page_num + 1}: {str(e)}")
                continue
    except Exception as e:
        return f"Error reading PDF file: {e}"
    return text
import re
import json

def predict_topics_from_papers(paper_content, num_topics=5):
    """
    Predicts key topics with importance percentage and details.
    Uses Gemini 1.5 Flash (free tier) with stricter JSON enforcement.
    """
    prompt = f"""
    Analyze the following question paper content and identify the {num_topics} most important topics.

    For each topic, provide:
    - "topic": Topic name (short and clear)
    - "importance": Integer 0-100 (importance for the exam)
    - "details": Short summary (1-2 sentences)

    Respond ONLY in JSON format inside triple backticks, like:
    ```json
    [
        {{
            "topic": "Operating System Structure",
            "importance": 90,
            "details": "Covers OS components, architecture, and key functions."
        }}
    ]
    ```

    Content:
    {paper_content}
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        text_out = getattr(response, 'text',
                           response.candidates[0].content.parts[0].text if response.candidates else "")

        # Extract JSON from code block if present
        json_match = re.search(r"```json\s*(\[\s*{.*}\s*\])\s*```", text_out, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = text_out.strip()

        topics_data = json.loads(json_str)
        return topics_data

    except json.JSONDecodeError as e:
        return [{"topic": f"JSON parse error: {e}", "importance": 0, "details": text_out}]
    except Exception as e:
        return [{"topic": f"Error predicting topics: {e}", "importance": 0, "details": ""}]
