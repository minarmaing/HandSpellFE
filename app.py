import streamlit as st
import requests

st.set_page_config(page_title="HandSpell Reader", layout="centered")
st.title("✋ HandSpell Reader")
st.write("Upload a hand sign image to predict the letter.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file, width=300)
    st.write("")
    st.write("Classifying...")

    response = requests.post(
        st.secrets["API_URL"],
        files={
            "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
        },
        timeout=120,
    )
    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted letter: {result['letter']}")
        st.write(f"Model score: {result['confidence']:.1%}")
    else:
        st.error(f"Error {response.status_code}: {response.text}")
