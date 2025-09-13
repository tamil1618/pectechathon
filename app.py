# Filename: genai_local_business_demo.py

import streamlit as st
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Sidebar: Add / Select Business ---
st.sidebar.title("Business Profiles")

# Stored business profiles (in-memory for demo; use DB for real app)
if "businesses" not in st.session_state:
    st.session_state.businesses = {}

# Add new business
st.sidebar.subheader("Add New Business")
business_name = st.sidebar.text_input("Business Name")
language = st.sidebar.selectbox("Language", ["English", "Tamil", "Hindi"])
tone = st.sidebar.selectbox("Tone", ["Friendly", "Formal", "Promotional"])
hashtags = st.sidebar.text_input("Hashtags (comma separated)")

if st.sidebar.button("Add Business") and business_name:
    st.session_state.businesses[business_name] = {
        "language": language,
        "tone": tone,
        "hashtags": hashtags.split(",") if hashtags else []
    }
    st.sidebar.success(f"{business_name} added!")

# Select a business to generate posts
st.sidebar.subheader("Select Business")
selected_business = st.sidebar.selectbox("Business", list(st.session_state.businesses.keys()))

st.title("GenAI for Local Businesses Demo")

if selected_business:
    business = st.session_state.businesses[selected_business]

    st.subheader(f"Generate Posts for: {selected_business}")

    product_name = st.text_input("Product / Service Name", "")
    event = st.text_input("Special Event / Occasion (optional)", "")
    
    if st.button("Generate Posts") and product_name:
        # Build AI prompt
        prompt = f"""
You are a marketing assistant trained for {selected_business}.
Language: {business['language']}
Tone: {business['tone']}
Hashtags: {', '.join(business['hashtags'])}
Create 3 social media posts for "{product_name}" {('for ' + event) if event else ''}.
Each post should be catchy, engaging, and suitable for Instagram or Facebook.
"""
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        ai_text = response.choices[0].message.content

        st.success("Generated Posts:")
        posts = ai_text.split("\n")
        for idx, post in enumerate(posts):
            if post.strip():
                st.markdown(f"**Post {idx+1}:** {post.strip()}")
                st.markdown("---")
