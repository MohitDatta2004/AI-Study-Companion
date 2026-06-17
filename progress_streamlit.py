import streamlit as st
from components.navbar import render_navbar

st.set_page_config(page_title="Progress | StudyGenie AI", page_icon="📈")
render_navbar()

st.title("📈 Your Study Progress")

st.markdown("### Activity Dashboard")

col1, col2, col3 = st.columns(3)

quizzes = len(st.session_state.get("quiz_data", [])) > 0
flashcards = len(st.session_state.get("flashcards_data", [])) > 0
messages = len(st.session_state.get("messages", []))

col1.metric("Quizzes Generated", "1" if quizzes else "0")
col2.metric("Flashcards Created", "1" if flashcards else "0")
col3.metric("Questions Asked", str(messages // 2))

st.divider()

st.markdown("### Study Plan Completion")
st.info("Drag the slider to update your progress for the current study plan.")

if "study_progress" not in st.session_state:
    st.session_state.study_progress = 0

progress_val = st.slider("Mark your current study plan progress (%)", 0, 100, st.session_state.study_progress)
st.session_state.study_progress = progress_val

st.progress(progress_val / 100.0)

if progress_val == 100:
    st.balloons()
    st.success("🎉 Congratulations! You have completed your study plan!")
