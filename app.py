import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from PIL import Image
import requests
import os

# ---------- CONFIG ----------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="VisualVibe",
    page_icon="🛍️",
    layout="wide"
)

# ---------- WEATHER ----------
def get_weather():
    try:
        loc = requests.get("https://ipinfo.io/json").json()
        city = loc.get("city", "Unknown")

        weather = requests.get(f"https://wttr.in/{city}?format=j1").json()
        temp = int(weather["current_condition"][0]["temp_C"])
        desc = weather["current_condition"][0]["weatherDesc"][0]["value"]

        return city, temp, desc
    except:
        return "Unknown", None, "Unavailable"

city, temp, condition = get_weather()

# ---------- UI HEADER ----------
st.markdown("""
<style>
.header {
    background:#131921;
    color:white;
    padding:15px;
    font-size:26px;
    font-weight:bold;
}
.card {
    border:1px solid #ddd;
    border-radius:10px;
    padding:15px;
}
</style>
<div class="header">🛍️ VisualVibe Advisor</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
menu = st.sidebar.radio(
    "Browse",
    ["🏠 Home", "🤖 AI Stylist", "🌦️ Weather Styling", "👔 Men", "👗 Women"]
)

# ---------- HOME ----------
if menu == "🏠 Home":
    st.subheader("Amazon-style Fashion Platform")
    col1, col2, col3 = st.columns(3)
    col1.markdown("<div class='card'>🤖 AI Styling</div>", unsafe_allow_html=True)
    col2.markdown("<div class='card'>🌦️ Weather Based</div>", unsafe_allow_html=True)
    col3.markdown("<div class='card'>🖼️ Fashion Gallery</div>", unsafe_allow_html=True)

# ---------- AI STYLIST ----------
elif menu == "🤖 AI Stylist":
    st.subheader("AI Fashion Advisor")

    gender = st.selectbox("Gender", ["Male", "Female"])
    occasion = st.selectbox("Occasion", ["Casual", "Formal", "Party"])

    uploaded = st.file_uploader(
        "Upload your photo (PNG / JPG)",
        type=["png", "jpg"]
    )

    if uploaded:
        st.image(Image.open(uploaded), width=250)

    if st.button("Get Recommendation"):
        prompt = f"""
        You are VisualVibe AI Fashion Advisor.
        Gender: {gender}
        Occasion: {occasion}
        Weather: {condition}, {temp}°C
        Suggest outfit, colors, footwear, accessories.
        """

        with st.spinner("Styling you..."):
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=250
            )

        st.success("Your Style Recommendation")
        st.write(res.choices[0].message.content)

# ---------- WEATHER ----------
elif menu == "🌦️ Weather Styling":
    st.subheader("Weather-Based Outfit")
    st.info(f"📍 Location: {city}")
    st.info(f"🌡️ Temperature: {temp}°C")
    st.info(f"☁️ Condition: {condition}")

# ---------- MEN ----------
elif menu == "👔 Men":
    st.subheader("Men's Collection")
    path = "images/men"
    cols = st.columns(3)

    if os.path.exists(path):
        for i, img in enumerate(os.listdir(path)):
            with cols[i % 3]:
                st.image(os.path.join(path, img), use_container_width=True)

# ---------- WOMEN ----------
elif menu == "👗 Women":
    st.subheader("Women's Collection")
    path = "images/women"
    cols = st.columns(3)

    if os.path.exists(path):
        for i, img in enumerate(os.listdir(path)):
            with cols[i % 3]:
                st.image(os.path.join(path, img), use_container_width=True)
