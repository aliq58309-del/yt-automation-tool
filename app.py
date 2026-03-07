import streamlit as st
import requests
import google.generativeai as genai

# Keys
GEMINI_API_KEY = "gen-lang-client-0059355912" 
PEXELS_API_KEY = "LqLYmxGJcYmvkNP3nP13WWSIVuAzGwHulanmPOGnWdkyNA9cGK10Wn8V"

# AI Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.title("🎥 YT Automation Video Finder")
user_script = st.text_area("Script Likhein:")

if st.button("Dhoondo!"):
    prompt = f"Give 3 keywords for this script: {user_script}. Only keywords, comma separated."
    response = model.generate_content(prompt)
    keywords = response.text.split(',')

    headers = {"Authorization": PEXELS_API_KEY}
    for kw in keywords:
        url = f"https://api.pexels.com/videos/search?query={kw.strip()}&per_page=1"
        res = requests.get(url, headers=headers).json()
        if res.get('videos'):
            st.video(res['videos'][0]['video_files'][0]['link'])
