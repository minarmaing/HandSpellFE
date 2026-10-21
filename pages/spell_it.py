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

st.session_state.random_word = take_random_word(list_words)

st.session_state.word_with_removed_letter, st.session_state.removed_letter = take_random_letter(st.session_state.random_word)

container = text_to_image_spellit(st.session_state.word_with_removed_letter)


uploaded_file = st.file_uploader("Guess the missing letter !", type=["jpg", "jpeg", "png"])


compare_predict(st.session_state.removed_letter, uploaded_file)

st.write(st.session_state.idx)

if st.button('Refresh'):
    #st.session_state.clear()
    st.write(st.session_state.idx)
    st.session_state.idx += 1
    st.write(st.session_state.idx)
    #st.rerun()
    #st.write(st.session_state.idx)
