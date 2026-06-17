import streamlit as st
from components.navbar import render_navbar

st.set_page_config(page_title="StudyGenie AI Home", page_icon="🧞", layout="wide")

st.title("🧞 StudyGenie AI")
st.markdown("""
### Your AI-Powered Study Assistant
Welcome to StudyGenie AI. This platform helps you study smarter by analyzing your study materials, answering questions, generating quizzes and flashcards, and creating custom study plans.

#### Features
- **💬 Smart Chatbot**: Ask questions about your notes.
- **📝 Quiz Generator**: Test your knowledge with AI-generated quizzes.
- **📇 Flashcards**: Memorize key concepts with flashcards.
- **📅 Study Planner**: Get a personalized study plan based on your exam date.
- **📊 Summary & Topics**: Extract important topics from your materials.

**👈 Get started by uploading your documents in the sidebar and selecting a tool!**
""")

render_navbar()
