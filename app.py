# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 21:05:05 2025

@author: Suprama
"""

# app.py

import streamlit as st
import requests

st.set_page_config(page_title="IELTS Tutor", layout="centered")
st.title("📝 IELTS Writing Feedback (GPT-4.1 via OpenRouter)")

essay = st.text_area("Paste your IELTS Writing Task essay here:", height=300)

if st.button("Get Feedback"):
    if not essay.strip():
        st.warning("Please enter your essay.")
    else:
        st.info("⏳ Please wait while GPT-4.1 evaluates your essay...")

        prompt = f"""
You are an IELTS examiner. Review this essay and provide:
- Band score (out of 9)
- Strengths
- Areas for improvement
- A revised version of the first paragraph

Essay:
\"\"\"
{essay}
\"\"\"
"""

        headers = {
            "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
            "HTTP-Referer": "ielts-tutor-llm-jzkl9fdtjjzauwmsbk2cif.streamlit.app",  # replace this with your app URL
            "X-Title": "IELTS Writing Feedback"
        }

        payload = {
            "model": "openai/gpt-4.1",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers=headers, json=payload)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            st.success("✅ Feedback generated:")
            st.markdown(reply)
        else:
            st.error(f"❌ Error: {response.status_code}\n{response.text}")
