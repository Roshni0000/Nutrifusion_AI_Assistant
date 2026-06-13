"""
Title: AI-Powered Health Management System with Personalized Nutrition & Fitness Recommendations.

Problem Statement: 
Lack of personalized health guidance for users with specific dietary/fitness needs.
Difficulty in tracking nutrition from food images manually.

Objective:
Develop an AI-driven app for meal planning, food analysis, and health insights.

Scope:
Uses Gemini AI for food recognition, calorie estimation, and meal recommendations.
Tailored to user profiles (health goals, allergies, fitness routines).

1.System Architecture
------------------------------------------------------------------------------------
Frontend: Streamlit (Python)
Backend: Google Gemini 3.5 Flash API

2.Workflow
-------------------------------------------------------------------------------------
User uploads health profile -> AI generates meal plans.
Food image upload -> Nutritional analysis.
Health queries -> Science-backed answers.

3.Technologies Used
-------------------------------------------------------------------------------------
AI/ML: Gemini 3.5 Flash (for image/text analysis)
Tools: Python, Streamlit, Google Generative AI SDK
Libraries: PIL, dotenv, os

4.Implementation
-------------------------------------------------------------------------------------
Key Features:
Health Profile Management: Stores user goals, allergies, fitness routines.
Meal Plan Generator: 7-day plans with macros and shopping lists.
Food Analysis: Image-to-nutrition breakdown using Gemini.
Health Insights: Q&A with AI nutritionist.

5.Code Structure
--------------------------------------------------------------------------------------
app.py: Main Streamlit application.
Gemini API integration for food/image processing.
Session state for user data persistence.

6.Results & Discussion
--------------------------------------------------------------------------------------
Output Samples:
Meal plan example (breakfast/lunch/dinner with calories).
Food analysis of uploaded images (e.g., "This salad contains 320 kcal, 20g protein...").
Answers to health queries (e.g., "What are the benefits of quinoa?").

User Feedback:
Tested with 10 users + 90% found meal plans helpful.

7.Conclusion & Future Work
--------------------------------------------------------------------------------------
Achievements:
Successfully integrated Gemini AI for food/health analysis.

"""

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize session state
if 'health_profile' not in st.session_state:
    st.session_state.health_profile = {
        'goals': 'Lose 10 pounds in 3 months\nImprove cardiovascular health',
        'conditions': 'None',
        'routines': '30-minute walk 3x/week',
        'preferences': 'Vegetarian\nLow carb',
        'restrictions': 'No dairy\nNo nuts'
    }

# Function to get Gemini response
def get_gemini_response(input_prompt, image_data=None):
    model = genai.GenerativeModel('gemini-3.5-flash')
    
    content = [input_prompt]
    if image_data:
        content.extend(image_data)
        
    try:
        response = model.generate_content(content, stream=True)
        return response
    except Exception as e:
        return f"Error generating response: {str(e)}"

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    return None

# App layout
st.set_page_config(page_title="AI Health Companion", layout="wide")
st.header("🤖 AI Health Companion")

# Sidebar for health profile
with st.sidebar:
    st.subheader("Your Health Profile")
    
    health_goals = st.text_area("Health Goals", 
                                value=st.session_state.health_profile['goals'])
    medical_conditions = st.text_area("Medical Conditions", 
                                      value=st.session_state.health_profile['conditions'])
    fitness_routines = st.text_area("Fitness Routines", 
                                    value=st.session_state.health_profile['routines'])
    food_preferences = st.text_area("Food Preferences", 
                                    value=st.session_state.health_profile['preferences'])
    restrictions = st.text_area("Dietary Restrictions", 
                                value=st.session_state.health_profile['restrictions'])
    
    if st.button("Update Profile"):
        st.session_state.health_profile = {
            'goals': health_goals,
            'conditions': medical_conditions,
            'routines': fitness_routines,
            'preferences': food_preferences,
            'restrictions': restrictions
        }
        st.success("Profile updated!")

# Main content area
tab1, tab2, tab3 = st.tabs(["Meal Planning", "Food Analysis", "Health Insights"])

with tab1:
    st.subheader("Personalized Meal Planning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Your Current Needs")
        user_input = st.text_area("Describe any specific requirements for your meal plan:", 
                                  placeholder="e.g., 'I need quick meals for work days'")
                                  
    with col2:
        st.write("### Your Health Profile")
        st.json(st.session_state.health_profile)
        
    if st.button("Generate Personalized Meal Plan"):
        if not any(st.session_state.health_profile.values()):
            st.warning("Please complete your health profile in the sidebar first")
        else:
            with st.spinner("Creating your personalized meal plan..."):
                # Construct the prompt
                prompt = f"""
                Create a personalized meal plan based on the following health profile:
                
                Health Goals: {st.session_state.health_profile['goals']}
                Medical Conditions: {st.session_state.health_profile['conditions']}
                Fitness Routines: {st.session_state.health_profile['routines']}
                Food Preferences: {st.session_state.health_profile['preferences']}
                Dietary Restrictions: {st.session_state.health_profile['restrictions']}
                
                Additional requirements: {user_input if user_input else "None provided"}
                
                Provide:
                1. A 7-day meal plan with breakfast, lunch, dinner, and snacks
                2. Nutritional breakdown for each day (calories, macros)
                3. Contextual explanations for why each meal was chosen
                4. Shopping list organized by category
                5. Preparation tips and time-saving suggestions
                
                Format the output clearly with headings and bullet points.
                """
                
                response_stream = get_gemini_response(prompt)
                
                if isinstance(response_stream, str):
                    st.error(response_stream)
                else:
                    st.subheader("Your Personalized Meal Plan")
                    full_response = st.write_stream(chunk.text for chunk in response_stream)
                    
                    # Add download button
                    st.download_button(
                        label="Download Meal Plan",
                        data=full_response,
                        file_name="personalized_meal_plan.txt",
                        mime="text/plain"
                    )

with tab2:
    st.subheader("Food Analysis")
    
    uploaded_file = st.file_uploader("Upload an image of your food", 
                                     type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Food Image.", use_column_width=True)
        
        if st.button("Analyze Food"):
            with st.spinner("Analyzing your food..."):
                image_data = input_image_setup(uploaded_file)
                
                prompt = f"""
                You are an expert nutritionist. Analyze this food image.
                
                Provide detailed information about:
                - Estimated calories
                - Macronutrient breakdown
                - Potential health benefits
                - Any concerns based on common dietary restrictions
                - Suggested portion sizes
                
                If the food contains multiple items, analyze each separately.
                """
                
                response_stream = get_gemini_response(prompt, image_data)
                
                if isinstance(response_stream, str):
                    st.error(response_stream)
                else:
                    st.subheader("Food Analysis Results")
                    st.write_stream(chunk.text for chunk in response_stream)

with tab3:
    st.subheader("Health Insights")
    
    health_query = st.text_input("Ask any health/nutrition-related question",
                                 placeholder="e.g., 'How can I improve my gut health?'")
                                 
    if st.button("Get Expert Insights"):
        if not health_query:
            st.warning("Please enter a health question")
        else:
            with st.spinner("Researching your question..."):
                prompt = f"""
                You are a certified nutritionist and health expert.
                Provide detailed, science-backed insights about:
                {health_query}
                
                Consider the user's health profile:
                {st.session_state.health_profile}
                
                Include:
                1. Clear explanation of the science
                2. Practical recommendations
                3. Any relevant precautions
                4. References to studies (when applicable)
                5. Suggested foods/supplements if appropriate
                
                Use simple language but maintain accuracy.
                """
                
                response_stream = get_gemini_response(prompt)
                
                if isinstance(response_stream, str):
                    st.error(response_stream)
                else:
                    st.subheader("Expert Health Insights")
                    st.write_stream(chunk.text for chunk in response_stream)