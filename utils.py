import os
import requests
import numpy as np
import streamlit as st

from PIL import Image, UnidentifiedImageError

API_BASE_URL = st.secrets["API_URL"]
API_SIGN_ENDPOINT = API_BASE_URL + 'sign/'
API_PREDICT_ENDPOINT = API_BASE_URL + 'predict'

list_words = ['Hello', 'Love', 'Website', 'No', 'Yes']

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

                st.image('raw_data/images/question mark.png',
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


def compare_predict(removed_letter, uploaded_file):

    if uploaded_file is not None:
        try:
            #image = Image.open(uploaded_file)
            #image.load()
            st.image(uploaded_file, width=300)
        except (UnidentifiedImageError, OSError, ValueError):
            st.error("Cannot read this image. Please upload another image.")
            st.stop()


    #try:
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
    #except (ValueError, KeyError, TypeError):
        #st.error("The prediction service returned an invalid response.")
    #except requests.RequestException as e:
        #st.error(f"Request failed: {e}")
        #st.stop()
        return st.write(removed_letter == result['letter'])

    else:
        st.write('Try a different image !')

#st.session_state.random_word = take_random_word(list_words)

#word_with_removed_letter, removed_letter = take_random_letter(st.session_state.random_word)
