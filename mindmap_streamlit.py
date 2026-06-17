import streamlit as st
from components.navbar import render_navbar

st.set_page_config(page_title="Mindmap | StudyGenie AI", page_icon="🧠")
render_navbar()

import requests
import streamlit.components.v1 as components

st.title("🧠 AI Mindmap Generator")

topic = st.text_input("Enter a topic to generate a mindmap")

if st.button("Generate Mindmap"):
    if topic:
        with st.spinner("Generating mindmap..."):
            try:
                response = requests.post("http://127.0.0.1:8000/generate-mindmap", json={"topic": topic})
                if response.status_code == 200:
                    data = response.json()
                    mermaid_code = data.get("mermaid_code", "")
                    
                    st.session_state.mindmap_code = mermaid_code
                    st.success("Mindmap generated!")
                else:
                    st.error("Failed to generate mindmap.")
            except Exception as e:
                st.error(f"Connection error: {e}")
    else:
        st.warning("Please enter a topic.")

if "mindmap_code" in st.session_state and st.session_state.mindmap_code:
    code = st.session_state.mindmap_code
    
    html = f"""
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
    <div class="mermaid">
    {code}
    </div>
    """
    
    st.markdown("### Your Mindmap")
    components.html(html, height=800, scrolling=True)
    
    with st.expander("View Raw Mermaid Code"):
        st.code(code, language="mermaid")
