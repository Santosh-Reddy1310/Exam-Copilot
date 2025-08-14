import PyPDF2
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv
import re
from collections import Counter

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_pdf(file):
    """
    Enhanced PDF text extraction with better error handling.
    """
    try:
        text = ""
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
        
        return text if text.strip() else "No text could be extracted from this PDF."
        
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def analyze_paper_structure(text):
    """
    Analyzes the structure of the exam paper to extract metadata.
    """
    analysis = {
        'total_questions': 0,
        'sections': [],
        'question_types': [],
        'marks_distribution': {},
        'time_allocation': '',
        'difficulty_indicators': []
    }
    
    try:
        # Count questions (basic pattern matching)
        question_patterns = [r'\b\d+\.\s', r'Q\d+', r'Question\s+\d+']
        question_count = 0
        for pattern in question_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            question_count = max(question_count, len(matches))
        
        analysis['total_questions'] = question_count
        
        # Identify sections
        section_patterns = [r'Section\s+[A-Z]', r'Part\s+[A-Z]', r'SECTION\s+[A-Z]']
        sections = []
        for pattern in section_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            sections.extend(matches)
        
        analysis['sections'] = list(set(sections))
        
        # Find marks mentions
        marks_pattern = r'\[(\d+)\s*marks?\]|\((\d+)\s*marks?\)|(\d+)\s*marks?'
        marks_mentions = re.findall(marks_pattern, text, re.IGNORECASE)
        
        # Extract difficulty indicators
        difficulty_keywords = ['easy', 'difficult', 'challenging', 'basic', 'advanced', 'complex']
        for keyword in difficulty_keywords:
            if keyword.lower() in text.lower():
                analysis['difficulty_indicators'].append(keyword)
        
        return analysis
        
    except Exception as e:
        print(f"Error in structure analysis: {str(e)}")
        return analysis

def predict_topics_from_papers(files):
    """
    Enhanced topic prediction with detailed analysis and formatting.
    """
    if not files:
        return "❌ No files provided for analysis."
    
    try:
        all_text = ""
        file_summaries = []
        
        # Process each file
        for i, file in enumerate(files):
            try:
                file.seek(0)  # Reset file pointer
                text = extract_text_from_pdf(file)
                
                if "Error reading PDF" in text or "No text could be extracted" in text:
                    file_summaries.append(f"⚠️ **{file.name}**: {text}")
                    continue
                
                all_text += f"\n\n=== PAPER {i+1}: {file.name} ===\n"
                all_text += text
                
                # Analyze structure
                structure = analyze_paper_structure(text)
                file_summaries.append(f"✅ **{file.name}**: {structure['total_questions']} questions, {len(structure['sections'])} sections")
                
            except Exception as e:
                file_summaries.append(f"❌ **{file.name}**: Error processing - {str(e)}")
        
        if not all_text.strip():
            return "❌ No valid content could be extracted from the uploaded files. Please check if the PDFs contain readable text."
        
        # Enhanced prompt for better analysis
        prompt = f"""
        You are an expert academic exam analyst with deep knowledge of educational patterns and assessment trends.
        
        **Task**: Analyze the following past exam papers and predict the most likely topics for the upcoming exam.
        
        **Instructions**:
        1. Identify recurring themes, topics, and question patterns
        2. Note the frequency and emphasis of different subjects
        3. Consider the progression and evolution of topics across papers
        4. Assess the complexity levels and question formats
        5. Predict topics based on gaps, patterns, and academic progression
        
        **Format your response as follows**:
        
        ## 📊 Analysis Summary
        - **Papers Analyzed**: {len([f for f in file_summaries if '✅' in f])}
        - **Key Patterns Identified**: [Brief overview of main patterns]
        - **Analysis Confidence**: [High/Medium/Low based on data quality]
        
        ## 🎯 Top 10 Predicted Topics
        
        | Rank | Topic | Probability | Preparation Focus | Reasoning |
        |------|-------|-------------|------------------|-----------|
        | 1 | [Topic Name] | [XX%] | [High/Medium/Low] | [Why this topic is likely] |
        | 2 | [Topic Name] | [XX%] | [High/Medium/Low] | [Why this topic is likely] |
        [Continue for all 10 topics...]
        
        ## 📈 Additional Insights
        
        ### 🔍 Question Format Patterns
        - [Observed question types and formats]
        
        ### ⚖️ Difficulty Distribution
        - [Expected difficulty levels and distribution]
        
        ### 🕒 Time Management Tips
        - [Recommendations based on observed paper structure]
        
        ### 🎓 Strategic Study Recommendations
        1. **High Priority**: Focus on topics ranked 1-4 (spend 50% of study time)
        2. **Medium Priority**: Topics ranked 5-7 (spend 30% of study time)  
        3. **Low Priority**: Topics ranked 8-10 (spend 20% of study time)
        
        ## ⚠️ Important Notes
        - [Any limitations or caveats about the prediction]
        - [Recommendations for additional preparation]
        
        **Past Papers Content**:
        {all_text[:15000]}  # Limit to avoid token limits
        """
        
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            return "❌ Failed to generate topic predictions. Please try again."
        
        # Add file processing summary at the beginning
        summary_section = "## 📁 File Processing Summary\n\n"
        for summary in file_summaries:
            summary_section += f"- {summary}\n"
        summary_section += "\n---\n\n"
        
        return summary_section + response.text
        
    except Exception as e:
        return f"❌ **Error during analysis**: {str(e)}\n\nPlease check your files and API configuration, then try again."

def get_topic_trends(all_text):
    """
    Analyzes trends in topic frequency across papers.
    """
    try:
        # Extract potential topics using keyword analysis
        common_academic_terms = [
            'algebra', 'calculus', 'geometry', 'statistics', 'probability',
            'physics', 'chemistry', 'biology', 'history', 'literature',
            'economics', 'psychology', 'sociology', 'philosophy',
            'programming', 'algorithm', 'database', 'network'
        ]
        
        topic_frequency = {}
        text_lower = all_text.lower()
        
        for term in common_academic_terms:
            count = text_lower.count(term)
            if count > 0:
                topic_frequency[term] = count
        
        return sorted(topic_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
        
    except Exception as e:
        return []

def extract_question_patterns(text):
    """
    Extracts common question patterns and formats.
    """
    patterns = {
        'multiple_choice': len(re.findall(r'\([a-d]\)', text, re.IGNORECASE)),
        'fill_blanks': len(re.findall(r'_{3,}', text)),
        'short_answer': len(re.findall(r'briefly|explain|define|what is', text, re.IGNORECASE)),
        'essay': len(re.findall(r'discuss|analyze|evaluate|essay', text, re.IGNORECASE)),
        'calculation': len(re.findall(r'calculate|compute|solve|find', text, re.IGNORECASE))
    }
    
    return {k: v for k, v in patterns.items() if v > 0}