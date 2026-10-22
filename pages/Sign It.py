import os
import requests
import numpy as np
import streamlit as st


from PIL import Image, UnidentifiedImageError
from utils import compare_predict
from style import load_style
load_style()

st.set_page_config(page_title="HandSpell Sign It", page_icon=".images/le-wagon-logo.png", layout="wide")

st.logo(".images/le-wagon-logo.png", size="large")

API_BASE_URL = st.secrets["API_URL"]

API_SIGN_ENDPOINT = API_BASE_URL + 'sign/'
API_PREDICT_ENDPOINT = API_BASE_URL + 'predict'

st.markdown(
    "# <span class='accent'>Sign</span> It",
    unsafe_allow_html=True,
)
st.subheader("Try making the Sign of this letter!")

LETTERS = list("ABCDEFGHIKLMNOPQRSTUVWXY")

random_letter = None

def take_random_letter(LETTERS: list=LETTERS):

    random_letter = np.random.choice(LETTERS, 1)

    return random_letter[0]

if st.button('Get a random letter!'):

    random_letter = take_random_letter(LETTERS)

    st.write(random_letter)


source = st.radio("Input", ["Upload image", "Take a photo"], horizontal=True)
upload = (st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"],
            key="single_upload") if source == "Upload image"
          else st.camera_input("Take a hand sign photo"))



if upload is not None:
    try:
        st.image(upload, width=300)
    except (UnidentifiedImageError, OSError, ValueError):
        st.error("Cannot read this image. Please upload another image.")
        st.stop()

    with st.spinner("Classifying..."):
        response = requests.post(
            API_PREDICT_ENDPOINT,
            files={
                "file": (
                    upload.name,
                    upload.getvalue(),
                    upload.type,
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


if result['letter'] == random_letter:

    st.write('You got the right sign !')

else:

    st.write('You got the wrong sign !')
