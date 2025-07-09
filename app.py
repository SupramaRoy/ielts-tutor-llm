# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 21:05:05 2025

@author: Suprama
"""

# app.py
import streamlit as st
import requests

st.set_page_config(page_title="IELTS Writing Tutor", layout="centered")
st.title("📝 IELTS Feedback (Free via Hugging Face)")

essay = st.text_area("Paste your IELTS essay below:", height=300)

if st.button("Get Feedback"):
    if not essay.strip():
        st.warning("⚠️ Please enter your essay.")
    else:
        st.info("⏳ Generating feedback...")

        # Define prompt for the model
        prompt = f"""
You are an IELTS examiner. Analyze the following essay and provide:
- Band score (out of 9)
- Strengths
- Areas for improvement
- Improved version of the first paragraph

Essay:
\"\"\"{essay}\"\"\"
"""

        headers = {
            "Authorization": f"Bearer {st.secrets['HF_API_TOKEN']}"
        }

        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 500, "temperature": 0.7}
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            output = result[0]["generated_text"]
            st.success("✅ Feedback generated!")
            st.markdown(output)
        else:
            st.error(f"❌ Error: {response.status_code}\n{response.text}")
