import os
import google.generativeai as genai
from dotenv import load_dotenv
import math
from datetime import datetime, timedelta

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def stress_test_plan(topics, hours_per_day, days_until_exam, context=None):
    """
    Enhanced study plan generator with advanced customization options.
    
    Args:
        topics (str): Comma-separated list of topics
        hours_per_day (int): Daily study hours
        days_until_exam (int): Days remaining until exam
        context (dict): Additional context with preferences
    """
    
    # Handle both old and new function signatures
    if context is None:
        context = {}
    
    # Extract context parameters with defaults
    intensity = context.get('intensity', 'Moderate')
    break_frequency = context.get('break_frequency', 'Every 45 mins')
    priority_topics = context.get('priority_topics', '')
    learning_style = context.get('learning_style', 'Mixed')
    
    # Parse topics
    topic_list = [topic.strip() for topic in topics.split(',') if topic.strip()]
    priority_list = [topic.strip() for topic in priority_topics.split(',') if topic.strip()]
    
    if not topic_list:
        return "❌ No valid topics provided. Please enter topics separated by commas."
    
    # Calculate study parameters
    total_study_hours = hours_per_day * days_until_exam
    revision_days = max(1, math.ceil(days_until_exam * 0.2))  # 20% for revision
    active_study_days = days_until_exam - revision_days
    
    # Intensity multipliers for different approaches
    intensity_config = {
        'Light': {'focus_time': 0.7, 'break_ratio': 0.3, 'revision_weight': 0.3},
        'Moderate': {'focus_time': 0.8, 'break_ratio': 0.2, 'revision_weight': 0.25},
        'Intensive': {'focus_time': 0.85, 'break_ratio': 0.15, 'revision_weight': 0.2},
        'Exam Mode': {'focus_time': 0.9, 'break_ratio': 0.1, 'revision_weight': 0.15}
    }
    
    config = intensity_config.get(intensity, intensity_config['Moderate'])
    
    # Learning style adaptations
    style_recommendations = {
        'Visual': "Include mind maps, diagrams, and flowcharts",
        'Auditory': "Include reading aloud, discussions, and audio materials",
        'Reading/Writing': "Focus on note-taking, summaries, and written exercises",
        'Kinesthetic': "Include hands-on practice, movement breaks, and interactive exercises",
        'Mixed': "Combine multiple approaches for comprehensive learning"
    }
    
    style_tip = style_recommendations.get(learning_style, style_recommendations['Mixed'])
    
    try:
        # Enhanced prompt for comprehensive study planning
        prompt = f"""
        You are an expert academic study planner and learning strategist with deep knowledge of cognitive science and effective study methodologies.
        
        **Student Profile**:
        - Study Intensity: {intensity}
        - Learning Style: {learning_style}
        - Break Preference: {break_frequency}
        - Daily Available Hours: {hours_per_day}
        - Days Until Exam: {days_until_exam}
        - Total Study Hours: {total_study_hours}
        
        **Topics to Cover**: {topics}
        **High Priority Topics**: {priority_topics if priority_topics else 'None specified'}
        
        **Planning Requirements**:
        1. Allocate {revision_days} days at the end for intensive revision
        2. Prioritize high-priority topics with 40% more time allocation
        3. Include {break_frequency.lower()} breaks in daily schedules
        4. Apply {intensity} study intensity throughout
        5. Adapt recommendations for {learning_style} learning style
        6. Include buffer time for unexpected delays
        7. Balance cognitive load throughout each day
        
        **Format your response as follows**:
        
        ## 📋 Personalized Study Plan Overview
        
        ### 📊 Plan Summary
        - **Study Period**: {days_until_exam} days ({active_study_days} active study + {revision_days} revision)
        - **Total Study Hours**: {total_study_hours} hours
        - **Daily Schedule**: {hours_per_day} hours/day with {break_frequency.lower()} breaks
        - **Intensity Level**: {intensity}
        - **Learning Style Focus**: {style_tip}
        
        ### 🎯 Topic Allocation Strategy
        | Topic | Priority | Allocated Hours | Study Days | Focus Areas |
        |-------|----------|-----------------|------------|-------------|
        [Create a detailed breakdown for each topic]
        
        ## 📅 Daily Study Schedule
        
        [Create a detailed day-by-day schedule in this format:]
        
        ### Day 1-{active_study_days}: Active Learning Phase
        
        **Day 1** | [Date would be today + 1]
        - **Morning Session (9:00-12:00)**: [Topic] - [Specific activities]
        - **Afternoon Session (14:00-17:00)**: [Topic] - [Specific activities] 
        - **Evening Session (19:00-21:00)**: [Review/Practice] - [Specific activities]
        - **Study Techniques**: [Specific methods based on learning style]
        - **Break Schedule**: {break_frequency} + 1-hour lunch + 30min evening break
        
        [Continue pattern for key days, then summarize middle days]
        
        ### Day {active_study_days + 1}-{days_until_exam}: Intensive Revision Phase
        
        **Day {active_study_days + 1}**: Complete Review Day 1
        - **Focus**: High-priority topics comprehensive review
        - **Method**: Active recall, practice tests, weak area identification
        
        [Continue revision schedule]
        
        ## 🧠 Study Optimization Tips
        
        ### 🎯 {Learning_Style} Learning Enhancements
        - [3-4 specific tips for their learning style]
        
        ### ⚡ {Intensity} Intensity Strategies
        - [Specific strategies for their chosen intensity level]
        
        ### 🕒 Time Management
        - [Practical time management tips]
        - [How to handle {break_frequency} breaks effectively]
        
        ## 📈 Progress Tracking
        
        ### Daily Checklist Template
        ```
        Day ___: Date: _______
        □ Morning session completed ({hours_per_day/3} hours)
        □ Afternoon session completed ({hours_per_day/3} hours)  
        □ Evening session completed ({hours_per_day/3} hours)
        □ All planned breaks taken
        □ Progress notes updated
        Mood: ___/10 | Energy: ___/10 | Comprehension: ___/10
        ```
        
        ### Weekly Review Points
        - [Key milestones to check each week]
        
        ## 🚨 Contingency Planning
        
        ### If You Fall Behind
        1. [Specific catch-up strategies]
        2. [Topics that can be shortened if needed]
        3. [Emergency revision tactics]
        
        ### Stress Management
        - [Techniques for handling study stress]
        - [Warning signs of burnout]
        - [Recovery strategies]
        
        ## 🎓 Final Week Strategy
        - [Detailed last-week preparation tactics]
        - [Day-before-exam routine]
        - [Exam day preparation]
        
        ## 📚 Recommended Resources
        - [Study tools and apps]
        - [Online resources]
        - [Physical materials needed]
        
        **Remember**: This plan is optimized for your {learning_style} learning style and {intensity} intensity preference. Adjust as needed based on your progress and energy levels.
        """
        
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            return "❌ Failed to generate study plan. Please try again."
        
        return response.text
        
    except Exception as e:
        return f"❌ **Error generating study plan**: {str(e)}\n\nPlease check your API configuration and try again."

def calculate_optimal_study_distribution(topics, total_hours, priority_topics):
    """
    Calculates optimal time distribution across topics based on priority and complexity.
    """
    try:
        topic_list = [topic.strip() for topic in topics.split(',') if topic.strip()]
        priority_list = [topic.strip().lower() for topic in priority_topics.split(',') if topic.strip()]
        
        base_hours_per_topic = total_hours / len(topic_list)
        topic_allocation = {}
        
        for topic in topic_list:
            if topic.lower() in priority_list:
                # Priority topics get 40% more time
                topic_allocation[topic] = round(base_hours_per_topic * 1.4, 1)
            else:
                topic_allocation[topic] = round(base_hours_per_topic * 0.8, 1)
        
        # Normalize to ensure total doesn't exceed available hours
        current_total = sum(topic_allocation.values())
        if current_total > total_hours:
            scaling_factor = total_hours / current_total
            for topic in topic_allocation:
                topic_allocation[topic] = round(topic_allocation[topic] * scaling_factor, 1)
        
        return topic_allocation
        
    except Exception as e:
        return {}

def generate_daily_breakdown(hours_per_day, break_frequency):
    """
    Generates optimal daily study session breakdown with breaks.
    """
    break_minutes = {
        'Every 25 mins (Pomodoro)': 25,
        'Every 45 mins': 45,
        'Every hour': 60,
        'Every 90 mins': 90
    }
    
    session_length = break_minutes.get(break_frequency, 45)
    total_minutes = hours_per_day * 60
    
    # Account for breaks (5 min break every session + 15 min for longer breaks)
    net_study_minutes = total_minutes * 0.8  # 20% for breaks
    
    sessions_per_day = math.ceil(net_study_minutes / session_length)
    
    return {
        'sessions_per_day': sessions_per_day,
        'minutes_per_session': session_length,
        'total_break_time': total_minutes - net_study_minutes,
        'recommended_schedule': generate_time_blocks(sessions_per_day, session_length)
    }

def generate_time_blocks(sessions, session_length):
    """
    Generates recommended time blocks for study sessions.
    """
    start_time = 9  # 9 AM start
    blocks = []
    
    for i in range(sessions):
        if i > 0:
            start_time += session_length / 60 + 0.25  # Add 15 min break
        
        if start_time >= 12 and start_time < 13:  # Lunch break
            start_time = 14  # Resume at 2 PM
        
        end_time = start_time + session_length / 60
        blocks.append(f"{int(start_time):02d}:{int((start_time % 1) * 60):02d}-{int(end_time):02d}:{int((end_time % 1) * 60):02d}")
        start_time = end_time
    
    return blocks

def get_study_recommendations(learning_style, intensity):
    """
    Provides specific study technique recommendations based on learning style and intensity.
    """
    base_techniques = {
        'Visual': ['Mind mapping', 'Flowcharts', 'Color coding', 'Visual summaries'],
        'Auditory': ['Reading aloud', 'Discussion groups', 'Audio recordings', 'Verbal repetition'],
        'Reading/Writing': ['Note-taking', 'Written summaries', 'Essay practice', 'Text analysis'],
        'Kinesthetic': ['Hands-on practice', 'Movement breaks', 'Interactive exercises', 'Physical models'],
        'Mixed': ['Combination approach', 'Multiple techniques', 'Varied methods', 'Flexible strategies']
    }
    
    intensity_modifiers = {
        'Light': 'with regular breaks and flexible pacing',
        'Moderate': 'with balanced intensity and structured breaks',
        'Intensive': 'with focused sessions and minimal breaks',
        'Exam Mode': 'with maximum concentration and timed practice'
    }
    
    techniques = base_techniques.get(learning_style, base_techniques['Mixed'])
    modifier = intensity_modifiers.get(intensity, intensity_modifiers['Moderate'])
    
    return f"Focus on {', '.join(techniques)} {modifier}"