import os
import google.generativeai as genai
from dotenv import load_dotenv

import streamlit as st
import os
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]


def explain_in_levels(concept, level="Intermediate", context=None):
    if isinstance(context, str):
        context = {'context': context}
    elif context is None:
        context = {}

    subject_context = context.get('context', '')
    explanation_style = context.get('style', 'Conversational')
    include_examples = context.get('include_examples', True)
    target_audience = context.get('audience', 'general public')

    prompt = (
        f"Explain '{concept}' at '{level}' level in '{explanation_style}' style "
        f"for '{target_audience}'."
    )
    if subject_context:
        prompt += f" Context: {subject_context}."
    if include_examples:
        prompt += " Include examples."

    try:
        # Use Gemini free-tier flash model
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return getattr(response, 'text',
                       response.candidates[0].content.parts[0].text if response.candidates else "")
    except Exception as e:
        return f"Error: {e}"
