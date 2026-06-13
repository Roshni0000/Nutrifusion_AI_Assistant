# Nutrifusion_AI_Assistant
An AI-powered health and nutrition companion built with Streamlit and Google Gemini 3.5 Flash. Features personalized 7-day meal planning, real-time multimodal food image analysis, and expert health insights.
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

