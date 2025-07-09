# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 21:05:05 2025

@author: Suprama
"""

# app.py
import streamlit as st
import requests

# Set Streamlit page settings
st.set_page_config(page_title="IELTS Writing Tutor", layout="centered")
st.title("📝 IELTS Writing Feedback (Free via Hugging Face API)")

# Input box for user essay
essay = st.text_area("Paste your IELTS Writing Task 2 essay below:", height=300)

# When button is clicked
if st.button("Get Feedback"):
    if not essay.strip():
        st.warning("⚠️ Please enter an essay before submitting.")
    else:
        st.info("⏳ Generating feedback... please wait.")

        # Prompt template
        prompt = f"""
You are an IELTS examiner. Carefully evaluate the following essay and provide:
1. Estimated IELTS Band score (out of 9)
2. Strengths of the essay
3. Areas for improvement
4. A revised version of the first paragraph

Essay:
\"\"\"
{essay}
\"\"\"
"""

        # Hugging Face Inference API settings
        headers = {
            "Authorization": f"Bearer {st.secrets['HF_API_TOKEN']}"
        }

        # ✅ Use this working public model
        API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

        # Request payload
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 500
            }
        }

        # Call Hugging Face Inference API
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            output = result[0]["generated_text"]
            st.success("✅ Feedback Generated!")
            st.markdown(output)
        else:
            st.error(f"❌ Error: {response.status_code}\n\n{response.text}")
