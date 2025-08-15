import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def stress_test_plan(topics, hours_per_day, days_until_exam, context=None):
    if context is None:
        context = {}

    intensity = context.get("intensity", "Moderate")
    break_frequency = context.get("break_frequency", "Every 45 mins")
    priority_topics = context.get("priority_topics", "")

    total_hours_available = hours_per_day * days_until_exam
    if not topics:
        return "Please provide at least one topic."
    hours_per_topic = total_hours_available / len(topics)

    prompt = f"""
    You are an expert academic planner. Create a **detailed daily timetable** for the next {days_until_exam} days.

    Inputs:
    - Topics: {", ".join(topics)}
    - Daily Study Hours: {hours_per_day}
    - Study Intensity: {intensity}
    - Break Frequency: {break_frequency}
    - Hours per topic: {hours_per_topic:.2f}

    The timetable should:
    1. Be structured **day-by-day** in a table format.
    2. Include **Morning**, **Afternoon**, **Evening** sessions.
    3. Assign topics to each session, ensuring all topics are covered.
    4. Include short breaks according to the break frequency.
    5. Balance revision and new learning.
    6. Mention the focus for each session.

    Format Example:
    ## Study Plan Overview
    - Days until exam: X
    - Daily hours: X
    - Intensity: X
    - Break frequency: X

    | Day | Morning Session | Afternoon Session | Evening Session |
    |-----|----------------|-------------------|-----------------|
    | 1   | Java - OOP Concepts | Probability - Basics | Operating Systems - Scheduling |
    | 2   | Digital Logic - Number Systems | Java - Exception Handling | Probability - Distributions |

    End with 3-5 general exam preparation tips.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return getattr(response, 'text',
                       response.candidates[0].content.parts[0].text if response.candidates else "")
    except Exception as e:
        return f"Error generating study plan: {e}"
