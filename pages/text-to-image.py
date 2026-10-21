import os
import requests
import numpy as np
import streamlit as st

from PIL import Image, UnidentifiedImageError


API_BASE_URL = st.secrets["API_URL"]

API_SIGN_ENDPOINT = API_BASE_URL + 'sign/'

st.set_page_config(page_title="HandSpell Text 2 Image", layout="centered")
st.title("Text 2 Image")
st.write("Input a Letter to get its Sign Language gesture.")

st.write(f"Connected to backend: {API_BASE_URL}")

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
