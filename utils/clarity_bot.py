import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def explain_in_levels(concept, level="Intermediate", context=None):
    """
    Explains a concept with enhanced customization options.
    
    Args:
        concept (str): The concept to explain
        level (str): Explanation level - "Beginner (ELI5)", "Intermediate", "Advanced", "Expert"
        context (dict): Enhanced context with style preferences
    """
    
    # Handle both old and new function signatures
    if isinstance(context, str):
        # Old signature: explain_in_levels(concept, level, subject_context)
        subject_context = context
        context = {'context': subject_context}
    elif context is None:
        context = {}
    
    # Extract context parameters with defaults
    subject_context = context.get('context', '')
    explanation_style = context.get('style', 'Conversational')
    include_examples = context.get('include_examples', True)
    include_visuals = context.get('include_visuals', True)
    follow_up_questions = context.get('follow_up_questions', True)
    explanation_length = context.get('length', 'Detailed')
    prerequisites = context.get('prerequisites', '')
    
    # Map UI level to explanation complexity
    level_mapping = {
        "Beginner (ELI5)": "elementary school level with simple analogies",
        "Intermediate": "high school level with clear explanations",
        "Advanced": "university level with technical depth",
        "Expert": "graduate/professional level with comprehensive detail"
    }
    
    complexity_level = level_mapping.get(level, "high school level with clear explanations")
    
    # Build style instructions
    style_instructions = {
        'Conversational': "Use a friendly, conversational tone as if explaining to a curious friend.",
        'Academic': "Use formal academic language with proper terminology and structured presentation.",
        'Step-by-step': "Break down the explanation into clear, numbered steps that build upon each other.",
        'Analogies & Examples': "Focus heavily on analogies, metaphors, and real-world comparisons."
    }
    
    style_prompt = style_instructions.get(explanation_style, style_instructions['Conversational'])
    
    # Build length instructions
    length_instructions = {
        'Concise': "Keep the explanation brief and to the point (2-3 paragraphs).",
        'Detailed': "Provide a thorough explanation with good depth (4-6 paragraphs).",
        'Comprehensive': "Give an extensive, comprehensive explanation covering all aspects (7+ paragraphs)."
    }
    
    length_prompt = length_instructions.get(explanation_length, length_instructions['Detailed'])
    
    # Construct the enhanced prompt
    prompt = f"""
    You are an expert educational AI tutor specializing in clear, adaptive explanations.
    
    **Task**: Explain the concept "{concept}" at {complexity_level}.
    
    **Subject Context**: {subject_context if subject_context else 'General knowledge'}
    
    **Style Requirements**: {style_prompt}
    
    **Length**: {length_prompt}
    
    **Prerequisites**: {prerequisites if prerequisites else 'Assume basic general knowledge'}
    
    **Additional Requirements**:
    """
    
    if include_examples:
        prompt += "\n- Include 2-3 practical, real-world examples that illustrate the concept"
    
    if include_visuals:
        prompt += "\n- Describe visual aids, diagrams, or mental images that would help understanding"
    
    prompt += f"""
    
    **Format your response as follows**:
    
    ## 🎯 Core Explanation
    [Main explanation of the concept]
    
    {"## 📝 Key Examples" if include_examples else ""}
    {("[Provide practical examples with brief explanations]" if include_examples else "")}
    
    {"## 🖼️ Visual Understanding" if include_visuals else ""}
    {("[Describe helpful visual representations or mental models]" if include_visuals else "")}
    
    ## 🔑 Key Takeaways
    - [3-5 bullet points summarizing the most important points]
    
    {"## ❓ Questions to Explore Further" if follow_up_questions else ""}
    {("[3-4 thoughtful follow-up questions to deepen understanding]" if follow_up_questions else "")}
    
    **Important**: 
    - Make sure the explanation matches the {level} level exactly
    - Use clear, engaging language appropriate for the chosen style
    - Ensure all technical terms are properly explained at the chosen level
    """
    
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text
        else:
            return "❌ Sorry, I couldn't generate an explanation right now. Please try again."
            
    except Exception as e:
        return f"❌ Error generating explanation: {str(e)}\n\nPlease check your API key and try again."

def get_concept_difficulty(concept, subject_context=""):
    """
    Analyzes the difficulty level of a concept to suggest appropriate explanation level.
    """
    prompt = f"""
    Analyze the difficulty level of this concept: "{concept}"
    Subject context: {subject_context}
    
    Rate the difficulty on a scale of 1-4:
    1 = Beginner (ELI5) - Elementary concepts
    2 = Intermediate - High school level
    3 = Advanced - University level  
    4 = Expert - Graduate/Professional level
    
    Respond with just the number and a brief reason.
    """
    
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text if response and response.text else "2 - Intermediate level assumed"
    except:
        return "2 - Intermediate level assumed"

def generate_related_concepts(concept, subject_context=""):
    """
    Generates related concepts that the user might want to learn about next.
    """
    prompt = f"""
    Given the concept "{concept}" in the context of {subject_context}, 
    suggest 5 related concepts that would be valuable to learn about next.
    
    Format as:
    1. Concept Name - Brief description
    2. Concept Name - Brief description
    [etc.]
    """
    
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text if response and response.text else ""
    except:
        return ""