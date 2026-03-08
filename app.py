import streamlit as st
import requests
import google.generativeai as genai

# --- CONFIGURATION (Keys Updated) ---
# Aapki di hui asli Gemini Key yahan set kar di hai
GEMINI_API_KEY = "AIzaSyDvGtzyZ9aB_1dVb5U66TMlzo1fVjXDGHI"
PEXELS_API_KEY = "LqLYmxGJcYmvkNP3nP13WWSIVuAzGwHulanmPOGnWdkyNA9cGK10Wn8V"

# AI Setup - Using Gemini 1.5 Flash (Fast and Free)
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- DASHBOARD DESIGN ---
st.set_page_config(page_title="AI Video Automator", page_icon="🎬")
st.title("🎬 YT Automation Video Finder")
st.write("Apni script likhein, AI khud clips dhoond kar layega.")

user_script = st.text_area("Script Likhein (e.g., A beautiful forest with sunlight):", height=150)

if st.button("Video Clips Dhoondo!"):
    if user_script:
        with st.spinner('AI analysis kar raha hai...'):
            try:
                # 1. Gemini se keywords nikalna
                prompt = f"Give me exactly 3 short search keywords for stock footage for this script: {user_script}. Only keywords, comma separated."
                response = model.generate_content(prompt)
                
                if response.text:
                    keywords = response.text.split(',')
                    st.success(f"🔍 AI Keywords: {response.text}")

                    # 2. Pexels se videos fetch karna
                    headers = {"Authorization": PEXELS_API_KEY}
                    
                    cols = st.columns(3) # 3 clips ko side-by-side dikhane ke liye
                    
                    for i, kw in enumerate(keywords):
                        kw = kw.strip()
                        url = f"https://api.pexels.com/videos/search?query={kw}&per_page=1"
                        res = requests.get(url, headers=headers).json()
                        
                        if 'videos' in res and len(res['videos']) > 0:
                            video_url = res['videos'][0]['video_files'][0]['link']
                            with cols[i % 3]:
                                st.write(f"**Clip: {kw}**")
                                st.video(video_url)
                        else:
                            with cols[i % 3]:
                                st.warning(f"'{kw}' nahi mili.")
                else:
                    st.error("AI ne koi keywords nahi diye.")
                    
            except Exception as e:
                st.error(f"⚠️ Technical Masla: {e}")
    else:
        st.warning("Pehle script likhein!")

st.markdown("---")
st.caption("AI Copilot Tool | Powered by Gemini & Pexels")
