import streamlit as st
import requests
from components.navbar import render_navbar

st.set_page_config(page_title="Quiz Generator | StudyGenie AI", page_icon="📝", layout="wide")
render_navbar()

st.title("📝 AI Quiz Generator")

topic = st.text_input("Enter a topic to generate a quiz for (e.g., 'Machine Learning')")
num_questions = st.slider("Number of questions", min_value=1, max_value=20, value=5)

if st.button("Generate Quiz"):
    if topic:
        with st.spinner("Generating quiz..."):
            try:
                response = requests.post("http://127.0.0.1:8000/generate-quiz", json={
                    "topic": topic,
                    "num_questions": num_questions
                })
                if response.status_code == 200:
                    data = response.json()
                    quiz = data.get("quiz", [])
                    st.session_state.quiz_data = quiz
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.success("Quiz generated!")
                else:
                    st.error("Failed to generate quiz.")
            except Exception as e:
                st.error(f"Connection error: {e}")
    else:
        st.warning("Please enter a topic.")

if "quiz_data" in st.session_state:
    quiz_data = st.session_state.quiz_data
    if isinstance(quiz_data, list) and len(quiz_data) > 0:
        st.markdown("### Your Quiz")

        quiz_answers = st.session_state.get("quiz_answers", {})
        submitted = st.session_state.get("quiz_submitted", False)

        for i, q in enumerate(quiz_data):
            st.divider()
            st.markdown(f"**Q{i+1}: {q.get('question','').strip()}**")
            options = q.get("options", {}) or {}

            choice = st.radio(
                label="Select an answer",
                options=["A", "B", "C", "D"],
                format_func=lambda k: f"{k}) {options.get(k,'')}",
                key=f"quiz_q_{i}",
                index=(["A", "B", "C", "D"].index(quiz_answers.get(str(i), "A")) if str(i) in quiz_answers else 0),
                disabled=submitted,
            )
            quiz_answers[str(i)] = choice

            if submitted:
                correct = q.get("answer")
                if choice == correct:
                    st.success(f"Correct. Answer: {correct}")
                else:
                    st.error(f"Incorrect. Correct answer: {correct} (you chose {choice})")
                st.info(q.get("explanation", ""))

        st.session_state.quiz_answers = quiz_answers

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Submit Quiz", disabled=submitted):
                st.session_state.quiz_submitted = True
                st.rerun()
        with col2:
            if submitted:
                correct_count = 0
                for i, q in enumerate(quiz_data):
                    if quiz_answers.get(str(i)) == q.get("answer"):
                        correct_count += 1
                st.metric("Score", f"{correct_count}/{len(quiz_data)}")
    elif isinstance(quiz_data, dict) and "raw_output" in quiz_data:
        st.error("Failed to parse AI output into strict JSON. Showing raw AI output instead:")
        if "validation_error" in quiz_data:
            st.warning(f"Validation error: {quiz_data.get('validation_error')}")
        if "parse_error" in quiz_data:
            st.warning(f"Parse error: {quiz_data.get('parse_error')}")
        st.code(str(quiz_data["raw_output"]))
    else:
        st.write("No quiz questions were generated. Data structure:", quiz_data)
