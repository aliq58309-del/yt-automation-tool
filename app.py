import streamlit as st
import requests
import google.generativeai as genai

# Keys
GEMINI_API_KEY = "AIzaSyDvGtzyZ9aB_1dVb5U66TMlzo1fVjXDGHI"
PEXELS_API_KEY = "LqLYmxGJcYmvkNP3nP13WWSIVuAzGwHulanmPOGnWdkyNA9cGK10Wn8V"

# AI Setup
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Gemini 3 Flash (1.5 Flash) is designed for speed and reliability
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Setup Error: {e}")

st.title("🎥 YT Automation Video Finder")
user_script = st.text_area("Script Likhein:")

if st.button("Video Clips Dhoondo!"):
    if user_script:
        with st.spinner('AI dhoond raha hai...'):
            try:
                # Prompting the model for visual keywords
                response = model.generate_content(f"Keywords for: {user_script}. 3 words only, comma separated.")
                keywords = response.text.split(',')
                
                headers = {"Authorization": PEXELS_API_KEY}
                for kw in keywords:
                    url = f"https://api.pexels.com/videos/search?query={kw.strip()}&per_page=1"
                    res = requests.get(url, headers=headers).json()
                    if 'videos' in res and len(res['videos']) > 0:
                        st.video(res['videos'][0]['video_files'][0]['link'])
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
