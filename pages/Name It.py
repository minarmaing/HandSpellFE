import os
import requests
import numpy as np
import streamlit as st

from PIL import Image, UnidentifiedImageError

from style import load_style
load_style()

API_BASE_URL = st.secrets["API_URL"]

API_SIGN_ENDPOINT = API_BASE_URL + 'sign/'
API_PREDICT_ENDPOINT = API_BASE_URL + 'predict'

st.set_page_config(page_title="HandSpell Name It", page_icon=".images/le-wagon-logo.png", layout="wide")

st.logo(".images/le-wagon-logo.png", size="large")

st.markdown(
    "# <span class='accent'>Name</span> It",
    unsafe_allow_html=True,
)

st.subheader("Guess what sign this is!")

LETTERS = list("ABCDEFGHIKLMNOPQRSTUVWXY")


def random_image():
    r = np.random.choice(len(LETTERS))
    letter = LETTERS[r]
    image_path = f'.images/ASL Letter Reference/{letter}.jpg'
    return letter, image_path


if st.button("Get a new letter image !", width=400):
    st.session_state.nameit_true_letter, st.session_state.nameit_image_path = random_image()
    st.session_state.nameit_guess = ""  # clear the previous guess

if "nameit_image_path" in st.session_state:
    st.image(st.session_state.nameit_image_path)

    letter = st.text_input("Guess the Letter!", max_chars=1, width=400, key="nameit_guess")

    if letter:
        true_letter = st.session_state.nameit_true_letter
        if letter.lower() == true_letter.lower():
            st.write(f"You guessed it right, the sign represents {true_letter} !")
        else:
            st.write(f"You guessed it wrong, try again !")
