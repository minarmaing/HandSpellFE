import streamlit as st


st.title('HandSpell')

st.markdown('# Reading hands, one letter at a time')



st.markdown(
    """
    HandSpell is a ASL Sign Language Translator, currently working only with
    with FingerSpelling.
    \n  \n
    \n\n**On HandSpell you can either translate, learn or play!**

    Translation currently works both ways, from image to text and text to image.

    And there's also the Spell It game to try what you've learned in ASL Sign Language !
    """
)

st.write("Not multi-\nline")
st.write("Still not multi- \nline")
st.write("Ok now it's multi-   \nline")
