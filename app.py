import streamlit as st
import requests
import google.generativeai as genai

# --- KEYS ---
GEMINI_API_KEY = "AIzaSyDvGtzyZ9aB_1dVb5U66TMlzo1fVjXDGHI"
PEXELS_API_KEY = "LqLYmxGJcYmvkNP3nP13WWSIVuAzGwHulanmPOGnWdkyNA9cGK10Wn8V"

# AI Setup - Version fix ke sath
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Naye models ke liye 'gemini-1.5-flash-latest' sab se behtar hai
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Setup Error: {e}")

st.title("🎥 YT Automation Video Finder")
user_script = st.text_area("Apni Script Likhein:")

if st.button("Video Clips Dhoondo!"):
    if user_script:
        with st.spinner('AI clips dhoond raha hai...'):
            try:
                # Gemini se keywords lena
                response = model.generate_content(f"Extract 3 visual keywords for stock footage from this script: {user_script}. Return only keywords separated by commas.")
                
                if response.text:
                    keywords = response.text.split(',')
                    st.success(f"🔍 Keywords: {response.text}")

                    # Pexels se videos lena
                    headers = {"Authorization": PEXELS_API_KEY}
                    for kw in keywords:
                        url = f"https://api.pexels.com/videos/search?query={kw.strip()}&per_page=1"
                        res = requests.get(url, headers=headers).json()
                        if res.get('videos'):
                            st.video(res['videos'][0]['video_files'][0]['link'])
            except Exception as e:
                st.error(f"⚠️ Technical Masla: {e}")
    else:
        st.warning("Pehle script likhein!")
