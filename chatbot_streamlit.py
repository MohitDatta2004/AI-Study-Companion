import streamlit as st
import requests
from components.navbar import render_navbar

st.set_page_config(page_title="Chatbot | StudyGenie AI", page_icon="💬")
render_navbar()

st.title("💬 Chat with your Notes")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your study materials..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Send last 5 messages as context to prevent context limits
                recent_history = st.session_state.messages[-6:-1]
                response = requests.post("http://127.0.0.1:8000/chat", json={
                    "question": prompt,
                    "history": recent_history
                })
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer provided.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    with st.expander("View Context Used"):
                        st.json(response.json().get("context_used", []))
                else:
                    st.error("Error communicating with AI.")
            except Exception as e:
                st.error(f"Connection error: {e}")
