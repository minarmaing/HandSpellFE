import os
import streamlit as st
import requests

from PIL import Image, UnidentifiedImageError
from style import load_style
load_style()

st.logo(".images/le-wagon-logo.png", size="large")

API_BASE_URL = st.secrets["API_URL"]

API_SIGN_ENDPOINT = API_BASE_URL + 'sign/'
API_PREDICT_ENDPOINT = API_BASE_URL + 'predict'

#st.set_page_config(page_title="HandSpell Reader", layout="centered")
#st.title("Image 2 Text")
#st.write("Upload a hand sign image to predict the letter.")

st.markdown(
    "# Image 2 <span class='accent'>Text</span>",
    unsafe_allow_html=True,
)
st.subheader("Upload a hand sign image to predict the letter !")

#st.write(f"Connected to backend: {API_BASE_URL}")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        image.load()
        st.image(image, width=300)
    except (UnidentifiedImageError, OSError, ValueError):
        st.error("Cannot read this image. Please upload another image.")
        st.stop()

    try:
        with st.spinner("Classifying..."):
            response = requests.post(
                API_PREDICT_ENDPOINT,
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    )
                },
                timeout=120,
            )
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted letter: {result['letter']}")
            st.write(f"Model score: {result['confidence']:.1%}")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except (ValueError, KeyError, TypeError):
        st.error("The prediction service returned an invalid response.")
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
        st.stop()




#st.title("Text 2 Image")
#st.write("Input a Letter to get its Sign Language gesture.")

st.markdown(
    "# Text 2 <span class='accent'>Image</span>",
    unsafe_allow_html=True,
)
st.subheader("Input a Letter to get its Sign Language gesture !")

LETTERS = list("ABCDEFGHIKLMNOPQRSTUVWXY")

letter = st.text_input('Letter', max_chars=1)

letter = letter.upper()

if letter in LETTERS:
    st.write("Pumba approves")

    try:
        with st.spinner("Getting image..."):
           response = requests.get(
               API_SIGN_ENDPOINT+letter,
               timeout=120
           )

        if response.status_code == 200:
            result = st.image(response.content)
            #st.success(f"Predicted letter: {result['letter']}")
            #st.write(f"Model score: {result['confidence']:.1%}")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except (ValueError, KeyError, TypeError) as e:
        st.write(e)
        st.error("The prediction service returned an invalid response.")
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
        st.stop()

else:
    st.write("Pumba is telling you to try a different letter -_-")
