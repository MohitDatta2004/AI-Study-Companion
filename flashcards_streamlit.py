import streamlit as st
import requests
from components.navbar import render_navbar

st.set_page_config(page_title="Flashcards | StudyGenie AI", page_icon="📇", layout="wide")
render_navbar()

st.title("📇 AI Flashcards")

topic = st.text_input("Enter a topic for flashcards")
num_cards = st.slider("Number of flashcards", min_value=1, max_value=20, value=5)

if st.button("Generate Flashcards"):
    if topic:
        with st.spinner("Generating flashcards..."):
            try:
                response = requests.post("http://127.0.0.1:8000/generate-flashcards", json={
                    "topic": topic,
                    "num_cards": num_cards
                })
                if response.status_code == 200:
                    data = response.json()
                    flashcards = data.get("flashcards", [])
                    st.session_state.flashcards_data = flashcards
                    st.success("Flashcards generated!")
                else:
                    st.error("Failed to generate flashcards.")
            except Exception as e:
                st.error(f"Connection error: {e}")
    else:
        st.warning("Please enter a topic.")

if "flashcards_data" in st.session_state:
    flashcards_data = st.session_state.flashcards_data
    if isinstance(flashcards_data, list) and len(flashcards_data) > 0:
        st.markdown("### Your Flashcards")
        cols = st.columns(2)
        for i, card in enumerate(flashcards_data):
            with cols[i % 2]:
                with st.container(border=True):
                    st.markdown(f"**Q{i+1}.** {card.get('question','')}")
                    with st.expander("Show answer"):
                        st.markdown(card.get("answer", ""))
    elif isinstance(flashcards_data, dict) and "raw_output" in flashcards_data:
        st.error("Failed to parse AI output into strict JSON. Showing raw AI output instead:")
        if "validation_error" in flashcards_data:
            st.warning(f"Validation error: {flashcards_data.get('validation_error')}")
        if "parse_error" in flashcards_data:
            st.warning(f"Parse error: {flashcards_data.get('parse_error')}")
        st.code(str(flashcards_data["raw_output"]))
    else:
        st.write("No flashcards were generated. Data structure:", flashcards_data)
