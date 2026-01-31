import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from PIL import Image
import os

# ---------- SETUP ----------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="VisualVibe",
    page_icon="🛍️",
    layout="wide"
)

# ---------- SESSION ----------
if "saved" not in st.session_state:
    st.session_state.saved = []

# ---------- STYLES ----------
st.markdown("""
<style>
.header {
    background-color: #131921;
    color: white;
    padding: 15px;
    font-size: 26px;
    font-weight: bold;
}
.card {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    background: white;
}
.save-btn {
    background-color: #ffa41c;
    color: black;
    padding: 8px;
    border-radius: 5px;
    text-align: center;
}
</style>
<div class="header">🛍️ VisualVibe — Amazon of Style</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
menu = st.sidebar.radio(
    "Shop by Category",
    [
        "🏠 Home",
        "🤖 AI Styling",
        "🎨 No Photo Styling",
        "🌦️ Weather Styling",
        "👔 Men",
        "👗 Women",
        "❤️ Saved"
    ]
)

# ---------- HOME ----------
if menu == "🏠 Home":
    st.subheader("Trending Styles")

    cols = st.columns(4)
    trends = ["Men Casual", "Women Party", "Winter Fits", "Office Wear"]
    for col, item in zip(cols, trends):
        with col:
            st.markdown(f"<div class='card'>🔥 {item}</div>", unsafe_allow_html=True)

# ---------- AI STYLING ----------
elif menu == "🤖 AI Styling":
    st.subheader("AI Fashion Advisor")

    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        occasion = st.selectbox("Occasion", ["Casual", "Formal", "Party"])
        image = st.file_uploader("Upload photo (optional)", type=["jpg", "png"])

        if image:
            st.image(Image.open(image), width=200)

        if st.button("Get AI Recommendation"):
            with st.spinner("Styling you..."):
                prompt = f"""
                You are VisualVibe AI Fashion Advisor.
                Gender: {gender}
                Occasion: {occasion}
                Suggest outfit, colors, footwear, accessories.
                """

                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=250
                )

                outfit = res.choices[0].message.content
                st.success("Your Style")
                st.write(outfit)

                if st.button("❤️ Save Outfit"):
                    st.session_state.saved.append(outfit)

# ---------- NO PHOTO ----------
elif menu == "🎨 No Photo Styling":
    st.subheader("Style Without Photo")

    color = st.selectbox("Base Color", ["Black", "White", "Blue", "Red"])
    occasion = st.selectbox("Occasion", ["Casual", "Formal", "Party"])

    suggestion = f"{color} themed outfit for {occasion}"
    st.info(suggestion)

    if st.button("❤️ Save"):
        st.session_state.saved.append(suggestion)

# ---------- WEATHER ----------
elif menu == "🌦️ Weather Styling":
    st.subheader("Weather Based Styling")

    weather = st.selectbox("Weather", ["Hot", "Cold", "Rainy"])

    tips = {
        "Hot": "Light cotton clothes, bright colors",
        "Cold": "Layered outfits, jackets, boots",
        "Rainy": "Waterproof jacket, dark colors"
    }

    st.success(tips[weather])

# ---------- MEN ----------
elif menu == "👔 Men":
    st.subheader("Men's Collection")
    cols = st.columns(3)

    items = ["Casual Wear", "Formal Wear", "Party Wear"]
    for col, item in zip(cols, items):
        with col:
            st.image("https://via.placeholder.com/250x350?text=" + item.replace(" ", "+"))
            st.caption(item)

# ---------- WOMEN ----------
elif menu == "👗 Women":
    st.subheader("Women's Collection")
    cols = st.columns(3)

    items = ["Casual Wear", "Formal Wear", "Party Wear"]
    for col, item in zip(cols, items):
        with col:
            st.image("https://via.placeholder.com/250x350?text=" + item.replace(" ", "+"))
            st.caption(item)

# ---------- SAVED ----------
elif menu == "❤️ Saved":
    st.subheader("Saved Outfits")

    if not st.session_state.saved:
        st.info("No saved outfits yet")
    else:
        for i, outfit in enumerate(st.session_state.saved, 1):
            st.markdown(f"**{i}.** {outfit}")
