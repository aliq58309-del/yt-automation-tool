import streamlit as st
import requests
import google.generativeai as genai

# --- KEYS ---
# Yahan apni asli AIza wali key paste karein. Quotes (" ") ke darmiyan koi space na ho.
GEMINI_API_KEY = "AIzaSy..." # <--- Is line ko poora mita kar apni key likhein
PEXELS_API_KEY = "LqLYmxGJcYmvkNP3nP13WWSIVuAzGwHulanmPOGnWdkyNA9cGK10Wn8V"

# AI Setup
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Setup Error: {e}")

st.title("🎥 YT Automation Video Finder")

user_script = st.text_area("Script Likhein:")

if st.button("Dhoondo!"):
    if user_script:
        try:
            # Gemini se keywords mangna
            prompt = f"Extract 3 visual search keywords for stock footage from this: {user_script}. Return only keywords, comma separated."
            response = model.generate_content(prompt)
            
            # Agar Gemini sahi jawab de raha hai
            keywords = response.text.split(',')
            st.write(f"🔍 AI Keywords: {response.text}")

            headers = {"Authorization": PEXELS_API_KEY}
            for kw in keywords:
                url = f"https://api.pexels.com/videos/search?query={kw.strip()}&per_page=1"
                res = requests.get(url, headers=headers).json()
                
                if 'videos' in res and len(res['videos']) > 0:
                    video_url = res['videos'][0]['video_files'][0]['link']
                    st.video(video_url)
                else:
                    st.warning(f"'{kw}' ke liye video nahi mili.")
        except Exception as e:
            # Ye line aapko batayegi ke asal masla kya hai
            st.error(f"⚠️ Masla: {e}")
    else:
        st.warning("Pehle script likhein!")
