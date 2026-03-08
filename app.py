import streamlit as st
import requests
import google.generativeai as genai

# --- CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyDvGtzyZ9aB_1dVb5U66TMlzo1fVjXDGHI"
PEXELS_API_KEY = "LqLYmxGJcYmvkNP3nP13WWSIVuAzGwHulanmPOGnWdkyNA9cGK10Wn8V"

# AI Setup - Using 'gemini-pro' which is most stable
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Setup Error: {e}")

st.set_page_config(page_title="AI Video Automator", page_icon="🎬")
st.title("🎬 YT Automation Video Finder")

user_script = st.text_area("Script Likhein:", height=150)

if st.button("Video Clips Dhoondo!"):
    if user_script:
        with st.spinner('AI clips dhoond raha hai...'):
            try:
                # 1. Gemini se keywords nikalna
                prompt = f"Give me exactly 3 search keywords for stock footage for this script: {user_script}. Only keywords, comma separated."
                response = model.generate_content(prompt)
                
                if response.text:
                    keywords = response.text.split(',')
                    st.success(f"🔍 AI Keywords: {response.text}")

                    # 2. Pexels se videos fetch karna
                    headers = {"Authorization": PEXELS_API_KEY}
                    for kw in keywords:
                        kw = kw.strip()
                        url = f"https://api.pexels.com/videos/search?query={kw}&per_page=1"
                        res = requests.get(url, headers=headers).json()
                        
                        if 'videos' in res and len(res['videos']) > 0:
                            video_url = res['videos'][0]['video_files'][0]['link']
                            st.write(f"🎥 Clip for: **{kw}**")
                            st.video(video_url)
                        else:
                            st.warning(f"'{kw}' ke liye koi video nahi mili.")
            except Exception as e:
                st.error(f"⚠️ Masla: {e}")
    else:
        st.warning("Pehle script likhein!")
