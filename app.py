import streamlit as st
import requests
import google.generativeai as genai

# --- CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyDvGtzyZ9aB_1dVb5U66TMlzo1fVjXDGHI"
PEXELS_API_KEY = "LqLYmxGJcYmvkNP3nP13WWSIVuAzGwHulanmPOGnWdkyNA9cGK10Wn8V"

# AI Setup - Using 'gemini-1.0-pro' for maximum compatibility
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # 404 Error se bachne ke liye model name update kiya gaya hai
    model = genai.GenerativeModel('gemini-1.0-pro')
except Exception as e:
    st.error(f"Setup Error: {e}")

st.set_page_config(page_title="AI Video Automator", page_icon="🎬")
st.title("🎬 YT Automation Video Finder")

user_script = st.text_area("Apni Script Likhein:", height=150, placeholder="Example: Moon landing in 1969...")

if st.button("Video Clips Dhoondo!"):
    if user_script:
        with st.spinner('AI analysis kar raha hai...'):
            try:
                # 1. Gemini se keywords nikalna
                prompt = f"Give me exactly 3 search keywords for stock footage for this script: {user_script}. Return ONLY keywords separated by commas."
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
                else:
                    st.error("AI ne koi jawab nahi diya.")
            except Exception as e:
                st.error(f"⚠️ Masla: {e}")
    else:
        st.warning("Pehle script likhein!")

st.markdown("---")
st.caption("AI Video Finder | Powered by Gemini 1.0 Pro")
