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

def take_random_letter(LETTERS: list=LETTERS):

    random_letter = np.random.choice(LETTERS, 1)

    return random_letter[0]

def verify_result():

    random_letter = st.session_state.signit_letter

    result = st.session_state.signit_predicted_letter

    if random_letter == result:

        st.write('You guessed right!')

    else:

        st.write('You guessed wrong!')

if st.button('Get a random letter!'):

    random_letter = take_random_letter(LETTERS)

    st.session_state.signit_letter = random_letter

    #RESET session state VARIABLES KIND SIR

    st.session_state.signit_upload = ''
    #st.session_state.signit_image = ''
    st.session_state.signit_predicted_letter = ''

    st.write(random_letter)

if 'signit_letter' in st.session_state:

    source = st.radio("Input", ["Upload image", "Take a photo"], horizontal=True, key='signit_source')

if 'signit_source' in st.session_state:
    upload = (st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"],
                               key='signit_image') if source == "Upload image"
              else st.camera_input("Take a hand sign photo", key='signit_image'))



if 'signit_image' in st.session_state:
    try:
        st.image(st.session_state.signit_image, width=300)
    except (UnidentifiedImageError, OSError, ValueError):
        st.error("Cannot read this image. Please upload another image.")
        st.stop()

    with st.spinner("Classifying..."):
        upload = st.session_state.signit_image
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
        st.session_state.signit_predicted_letter = result['letter']
        st.success(f"Predicted letter: {result['letter']}")
        st.write(f"Model score: {result['confidence']:.1%}")
        verify_result()
    else:
        st.error(f"Error {response.status_code}: {response.text}")
