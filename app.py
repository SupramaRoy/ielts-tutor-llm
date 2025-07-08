# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 21:05:05 2025

@author: Suprama
"""

# app.py

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="IELTS Writing Tutor", layout="centered")

st.title("📝 IELTS Writing Feedback (LLM-powered)")

# Load API Key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# User input
essay = st.text_area("Paste your IELTS Writing Task essay here:", height=300)

if st.button("Get Feedback"):
    if essay.strip() == "":
        st.warning("Please enter an essay.")
    else:
        with st.spinner("Analyzing with GPT..."):
            prompt = f"""
You are an IELTS examiner. Analyze the following essay and provide:
1. Band score (out of 9)
2. Strengths
3. Areas of improvement
4. One revised version of the first paragraph

Essay:
\"\"\"
{essay}
\"\"\"
"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            feedback = response.choices[0].message.content
            st.success("✅ Feedback Generated!")
            st.markdown(feedback)
