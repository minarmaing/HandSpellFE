import os
import requests
import numpy as np
import streamlit as st

from PIL import Image, ImageOps, UnidentifiedImageError

API_BASE_URL = st.secrets["API_URL"]
API_SIGN_ENDPOINT = API_BASE_URL + 'sign/'
API_PREDICT_ENDPOINT = API_BASE_URL + 'predict'

CONFIDENCE_THRESHOLD = 0.3

list_words = ['Hello', 'Love', 'Website', 'No', 'Yes']


def process_image_for_show(upload):
    return ImageOps.exif_transpose(Image.open(upload))


def get_uploaded_image(uploaded_file):
    processed_upload = None
    if uploaded_file is not None:
        try:
            processed_upload = process_image_for_show(uploaded_file)
        except (UnidentifiedImageError, OSError, ValueError):
            st.error("Could not read this files. Please try a different image!")
            st.stop()
    return processed_upload


def take_random_word(list_of_words: list):

    #random_word = np.random.choice(list_of_words, 1)
    #st.session_state.idx = 0

    #random_word = list_of_words[st.session_state.idx]

    #st.write(random_word)

    #return random_word

    idx = st.session_state.idx

    return list_of_words[idx%len(list_of_words)]


def take_random_letter(word):

    r = np.random.choice(len(word))

    removed_letter = word[r]
    removed_letter = removed_letter.upper()

    random_word = []
    for index, letter in enumerate(list(word)):
        if index == r:
            random_word.append('_')
        else:
            random_word.append(letter)

    return "".join(random_word), removed_letter


def text_to_image_spellit(word: str):

    container = st.container(horizontal=True, wrap=True, border=True)

    with container:
        for letter in word:
            letter = letter.upper()
            if letter == '_':
                st.image('.images/question mark.png',
                         caption='?',
                         width=64)

            else:
                response = requests.get(
                    API_SIGN_ENDPOINT+letter,
                    timeout=120
                    )
                st.image(response.content,
                        caption=letter,
                        width=64)

    return container


def get_image_and_prediction(uploaded_file):

    processed_upload = get_uploaded_image(uploaded_file)
    predicted_letter = None
    prediction = None

    if processed_upload is not None:
        with st.spinner("Reading hand signs…"):
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
            prediction = response.json()
            if prediction["confidence"] is None:
                st.warning("No hand/sign detected. Try a clear photo of the whole hand.")
            else:
                predicted_letter = prediction["letter"]
        else:
            st.error(f"Error {response.status_code}: {response.text}")

    return processed_upload, predicted_letter, prediction
