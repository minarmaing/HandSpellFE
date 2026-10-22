import streamlit as st

from style import load_style
load_style()
st.html("""
<style>
h1 { font-size: 4rem !important; }
</style>
""")

st.logo(".images/le-wagon-logo.png", size="large")


st.markdown(
    "# Hand<span class='accent'>Spell</span>",
    unsafe_allow_html=True,
)
st.subheader("Reading hands, one letter at a time")

st.markdown(
    """
HandSpell is an ASL (American Sign Language) translator. For now, it works with fingerspelling: the signed alphabet.

**On HandSpell you can translate, learn or play!**

Translation works both ways: from image to text, and from text to image.

And there's the <span class='accent'>Spell it</span> game, to test what you've learned!
    """,
    unsafe_allow_html=True,
)
