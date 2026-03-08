import streamlit as st
import requests
import google.generativeai as genai

# --- CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyDvGtzyZ9aB_1dVb5U66TMlzo1fVjXDGHI"
PEXELS_API_KEY = "LqLYmxGJcYmvkNP3nP13WWSIVuAzGwHulanmPOGnWdkyNA9cGK10Wn8V"

# AI Setup - Version mismatch fix
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Sirf 'gemini-1.5-flash' likhein, '-latest' ya 'v1beta' nahi
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Setup Error: {e}")

st.title("🎥 YT Automation Video Finder")

user_script = st.text_area("Apni Script Likhein:", placeholder="Example: A futuristic city in 2050...")

if st.button("Video Clips Dhoondo!"):
    if user_script:
        with st.spinner('AI analysis kar raha hai...'):
            try:
                # Gemini se keywords mangna
                prompt = f"Extract 3 visual keywords for stock footage from this script: {user_script}. Return only keywords separated by commas."
                response = model.generate_content(prompt)
                
                if response and response.text:
                    keywords = response.text.split(',')
                    st.success(f"🔍 AI Keywords: {response.text}")

                    # Pexels API Call
                    headers = {"Authorization": PEXELS_API_KEY}
                    for kw in keywords:
                        kw = kw.strip()
                        url = f"https://api.pexels.com/videos/search?query={kw}&per_page=1"
                        res = requests.get(url, headers=headers).json()
                        
                        if 'videos' in res and len(res['videos']) > 0:
                            v_url = res['videos'][0]['video_files'][0]['link']
                            st.write(f"🎥 Clip for: **{kw}**")
                            st.video(v_url)
                        else:
                            st.info(f"'{kw}' ke liye video nahi mili.")
                else:
                    st.error("AI model busy hai, dubara try karein.")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
    else:
        st.warning("Pehle script likhein!")
