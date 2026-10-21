import os
import requests
import numpy as np
import streamlit as st

from PIL import Image, UnidentifiedImageError
from utils import text_to_image_spellit, take_random_letter, take_random_word, compare_predict, list_words #word_with_removed_letter, #removed_letter

st.set_page_config(page_title="HandSpell Spell It", layout="centered")
st.title("Spell it")
st.write("Complete the word with an image !")


#random_word = take_random_word(list_words)

#word_with_removed_letter, removed_letter = take_random_letter(random_word)

#st.session_state.random_word = take_random_word(list_words)

#st.session_state.word_with_removed_letter, st.session_state.removed_letter = take_random_letter(st.session_state.random_word)

if "idx" not in st.session_state:

    st.session_state.idx = 0

if "random_word" not in st.session_state:

    st.session_state.random_word = take_random_word(list_words)

    (st.session_state.word_with_removed_letter, st.session_state.removed_letter) = take_random_letter(st.session_state.random_word)

#container = text_to_image_spellit(st.session_state.word_with_removed_letter)

text_to_image_spellit(st.session_state.word_with_removed_letter)

enable_webcam = st.checkbox("Enable camera")
enable_upload = st.checkbox("Enable upload")
webcam_uploaded_file = st.camera_input("Guess the missing letter!", disabled=not enable_webcam)

st.write('Or')

uploaded_file = st.file_uploader("Upload an image !", type=["jpg", "jpeg", "png"], disabled=not enable_upload)


compare_predict(st.session_state.removed_letter, webcam_uploaded_file)


if st.button('Refresh'):

    st.session_state.idx = (st.session_state.idx+1)%len(list_words)

    st.session_state.random_word = take_random_word(list_words)

    (st.session_state.word_with_removed_letter, st.session_state.removed_letter) = take_random_letter(st.session_state.random_word)

    st.rerun()
