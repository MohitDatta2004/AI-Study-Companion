import streamlit as st
import requests
import pandas as pd
from components.navbar import render_navbar
from components.charts import render_bar_chart

st.set_page_config(page_title="Topics & Search | StudyGenie AI", page_icon="📊")
render_navbar()

st.title("📊 Summary, Topics & Search")

st.markdown("### 📝 AI Topic Summary")
topic_to_summarize = st.text_input("Enter a specific topic or question you want summarized:")

if st.button("Generate Topic Summary"):
    if topic_to_summarize:
        with st.spinner(f"Generating summary for '{topic_to_summarize}'..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/generate-summary",
                    json={"topic": topic_to_summarize}
                )
                if response.status_code == 200:
                    summary_data = response.json().get("summary", "")
                    st.session_state.overall_summary = summary_data
                    st.success("Summary generated successfully!")
                else:
                    st.error("Failed to generate summary.")
            except Exception as e:
                st.error(f"Connection error: {e}")
    else:
        st.warning("Please enter a topic to summarize.")

if "overall_summary" in st.session_state and st.session_state.overall_summary:
    st.info("Here is the summary of your requested topic:")
    st.markdown(st.session_state.overall_summary)

st.divider()

st.markdown("### Extracted Key Topics")
if st.button("Extract Important Topics from Notes"):
    with st.spinner("Analyzing documents..."):
        try:
            response = requests.get("http://127.0.0.1:8000/important-topics")
            if response.status_code == 200:
                data = response.json()
                topics = data.get("important_topics", [])
                if topics:
                    df = pd.DataFrame(topics, columns=["Topic", "Frequency"])
                    st.dataframe(df, use_container_width=True)
                    
                    render_bar_chart(df.set_index("Topic"))
                else:
                    st.info("No topics found. Please upload more documents.")
            else:
                st.error("Failed to extract topics.")
        except Exception as e:
            st.error(f"Connection error: {e}")

st.divider()

st.markdown("### Search Documents")
query = st.text_input("Search for specific information in your notes")
if st.button("Search"):
    if query:
        with st.spinner("Searching..."):
            try:
                response = requests.get(f"http://127.0.0.1:8000/search?query={query}")
                if response.status_code == 200:
                    results = response.json().get("results", [])
                    st.write(f"Found {len(results)} results:")
                    for res in results:
                        with st.expander(f"Source: {res.get('source')} (Score: {res.get('score')})"):
                            st.write(res.get('content'))
                else:
                    st.error("Search failed.")
            except Exception as e:
                st.error(f"Connection error: {e}")
