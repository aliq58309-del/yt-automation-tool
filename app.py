import streamlit as st
import requests
import google.generativeai as genai

# --- UPDATED KEYS ---
# Gemini Key (AIza se shuru honay wali)
GEMINI_API_KEY = "AIzaSyB..." # <--- Yahan apni wo puri AIza wali key paste karein jo image mein dikh rahi thi
PEXELS_API_KEY = "LqLYmxGJcYmvkNP3nP13WWSIVuAzGwHulanmPOGnWdkyNA9cGK10Wn8V"

# AI Setup - Using 1.5-Flash for better speed and stability
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="YT Automation Tool", page_icon="🎥")
st.title("🎥 YT Automation Video Finder")
st.write("Apni script likhein aur AI relevant clips dhoond layega.")

user_script = st.text_area("Script Likhein:", placeholder="Example: Space exploration and galaxies...")

if st.button("Dhoondo!"):
    if user_script:
        with st.spinner('AI analysis kar raha hai...'):
            try:
                # Gemini se keywords lena
                prompt = f"Give me exactly 3 search keywords for stock footage for this script: {user_script}. Only keywords, comma separated."
                response = model.generate_content(prompt)
                keywords = response.text.split(',')

                st.success(f"Keywords: {response.text}")

                # Pexels se videos fetch karna
                headers = {"Authorization": PEXELS_API_KEY}
                for kw in keywords:
                    kw = kw.strip()
                    url = f"https://api.pexels.com/videos/search?query={kw}&per_page=1"
                    res = requests.get(url, headers=headers).json()
                    
                    if res.get('videos') and len(res['videos']) > 0:
                        video_url = res['videos'][0]['video_files'][0]['link']
                        st.write(f"**Clip for: {kw}**")
                        st.video(video_url)
                    else:
                        st.warning(f"'{kw}' ke liye koi video nahi mili.")
            except Exception as e:
                st.error(f"Ek masla aa gaya hai: {e}")
    else:
        st.warning("Pehle kuch likhen toh sahi!")

st.markdown("---")
st.caption("Developed by Gemini AI | Free Automation Tool")
