import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from components.navbar import render_navbar

st.set_page_config(page_title="Study Planner | StudyGenie AI", page_icon="📅")
render_navbar()

st.title("📅 Smart Study Planner")

col1, col2 = st.columns(2)
with col1:
    exam_date = st.date_input("Exam Date", min_value=datetime.today())
with col2:
    hours_per_day = st.number_input("Study Hours per Day", min_value=1, max_value=12, value=3)

if st.button("Generate Study Plan"):
    with st.spinner("Analyzing PYQs and Notes to generate plan..."):
        try:
            response = requests.post("http://127.0.0.1:8000/generate-study-plan", json={
                "exam_date": exam_date.strftime("%Y-%m-%d"),
                "hours_per_day": hours_per_day
            })
            if response.status_code == 200:
                data = response.json()
                
                ranked_topics = data.get("ranked_topics", [])
                st.subheader("🎯 Ranked Topics by Importance")
                if ranked_topics:
                    df_topics = pd.DataFrame(ranked_topics, columns=["Topic", "Importance Score"])
                    st.dataframe(df_topics, use_container_width=True)
                
                study_plan = data.get("study_plan", [])
                if isinstance(study_plan, list) and len(study_plan) > 0:
                    st.subheader("🗓️ Your Daily Study Schedule")
                    for day_plan in study_plan:
                        with st.expander(f"{day_plan.get('date')} ({day_plan.get('study_hours')} Hours)"):
                            st.write("**Topics to cover:**")
                            for t in day_plan.get("topics", []):
                                st.write(f"- {t}")
                elif isinstance(study_plan, dict) and "error" in study_plan:
                    st.error(study_plan["error"])
                else:
                    st.warning("Could not generate a study plan. Make sure exam date is in the future and you have uploaded documents.")
            else:
                st.error("Failed to generate study plan.")
        except Exception as e:
            st.error(f"Connection error: {e}")
