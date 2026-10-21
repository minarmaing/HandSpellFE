import os
import requests
import numpy as np
import streamlit as st

from PIL import Image, UnidentifiedImageError

list_words = ['Hello', 'Love']

random_word = np.random.choice(list_words, 1)



def take_random_letter(random_letter):

    r = np.random.choice(len(random_letter))

    random_word = []

    for index, letter in enumerate(random_letter):

        if index == r:

            random_word.append('_')

        else:
            random_word.append(letter)



    return "".join(random_word)



print(take_random_letter('Love'))
