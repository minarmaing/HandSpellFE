import os
import requests
import numpy as np
import streamlit as st

from PIL import Image, UnidentifiedImageError
from utils import text_to_image_spellit, take_random_letter, take_random_word, compare_predict, list_words, random_word, word_with_removed_letter, removed_letter

st.set_page_config(page_title="HandSpell Spell It", layout="centered")
st.title("Spell it")
st.write("Complete the word with an image !")


#random_word = take_random_word(list_words)

#word_with_removed_letter, removed_letter = take_random_letter(random_word)

container = text_to_image_spellit(word_with_removed_letter, removed_letter)
