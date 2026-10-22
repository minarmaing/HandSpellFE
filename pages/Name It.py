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

CURRENT_LETTER = None

letter = None

if "get_image" not in st.session_state:
    st.session_state.a_done = False

def random_image():

    r = np.random.choice(len(LETTERS))

    CURRENT_LETTER = LETTERS[r]

    st.image(f'.images/ASL Letter Reference/{CURRENT_LETTER}.jpg')

    return CURRENT_LETTER

if st.button("Get a new letter image !", width=400):

    CURRENT_LETTER = random_image()

    letter = st.text_input('Guess the Letter!', max_chars=1, width=400)

    st.write(CURRENT_LETTER)

    st.session_state.get_image = True
#st.write(letter)

if letter:

    not st.session_state.get_image

    letter = letter.upper()

    if letter == CURRENT_LETTER:

        st.write(f'You guessed it right, the sign represents {letter} !')


    else:

        st.write(f'You guessed it wrong, the letter was {CURRENT_LETTER} try again !')
