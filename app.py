import streamlit as st
import requests
import google.generativeai as genai

# --- KEYS ---
# Yahan apni AI Studio wali AIza... wali key paste karein
GEMINI_API_KEY = "YAHAN_APNI_AIZA_WALI_KEY_DALEIN" 
PEXELS_API_KEY = "LqLYmxGJcYmvkNP3nP13WWSIVuAzGwHulanmPOGnWdkyNA9cGK10Wn8V"

# AI Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🎥 YT Automation Video Finder")

user_script = st.text_area("Script Likhein:")

if st.button("Dhoondo!"):
    if user_script:
        try:
            # AI se keywords mangna
            prompt = f"Extract 3 visual search keywords for stock footage from this: {user_script}. Return only keywords, comma separated."
            response = model.generate_content(prompt)
            keywords = response.text.split(',')

            st.write(f"Keywords: {response.text}")

            headers = {"Authorization": PEXELS_API_KEY}
            for kw in keywords:
                url = f"https://api.pexels.com/videos/search?query={kw.strip()}&per_page=1"
                res = requests.get(url, headers=headers).json()
                if 'videos' in res and len(res['videos']) > 0:
                    video_url = res['videos'][0]['video_files'][0]['link']
                    st.video(video_url)
        except Exception as e:
            st.error(f"Error: {e}")
