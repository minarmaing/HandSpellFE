import hashlib
import html
import io
import math
import os
import time

import requests
import streamlit as st

from urllib.parse import urlsplit, urlunsplit
from PIL import Image, ImageOps, UnidentifiedImageError
from style import load_style
load_style()

st.set_page_config(page_title="HandSpell Read It", page_icon=".images/le-wagon-logo.png", layout="wide")

st.logo(".images/le-wagon-logo.png", size="large")

API_BASE_URL = st.secrets["API_URL"]

API_SIGN_ENDPOINT = API_BASE_URL + 'sign/'
API_PREDICT_ENDPOINT = API_BASE_URL + 'predict'
MAX_BYTES = 10 * 1024 * 1024

NO_HAND = {"NO HAND", "NO HAND/SIGN", "NO_HAND"}
ALPHABET = set("ABCDEFGHIKLMNOPQRSTUVWXY")  # Static letters: excludes J and Z.

def prediction_url(value):
    """Accept either the API base URL or the complete /predict URL."""
    parts = urlsplit(value.strip())
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise ValueError("API_URL must be an http:// or https:// URL.")
    path = parts.path.rstrip("/")
    if not path.endswith("/predict"):
        path += "/predict"
    return urlunsplit((parts.scheme, parts.netloc, path, parts.query, ""))

def read_image(upload):
    raw = upload.getvalue()
    if len(raw) > MAX_BYTES:
        raise ValueError("Please use an image smaller than 10 MB.")
    with Image.open(io.BytesIO(raw)) as original:
        original.load()
        image = ImageOps.exif_transpose(original).convert("RGB")
    # Preview and inference use the same orientation and RGB pixels.
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return image, buffer.getvalue()

def normalize_result(payload):
    """Support the two response keys already used by the team's APIs."""
    if not isinstance(payload, dict):
        raise ValueError("API response must be a JSON object.")
    letter = payload.get("prediction") or payload.get("letter")
    if not isinstance(letter, str) or not letter.strip():
        raise ValueError("API response needs a 'prediction' or 'letter' string.")
    letter = letter.strip().upper()
    no_hand = letter in NO_HAND
    if not no_hand and letter not in ALPHABET:
        raise ValueError(f"Unsupported prediction: {letter}")
    confidence = payload.get("confidence")
    if confidence is not None:
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
            raise ValueError("Confidence must be a number between 0 and 1, or null.")
        if not math.isfinite(confidence) or not 0 <= confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1.")
    return {"letter": letter, "confidence": confidence, "no_hand": no_hand}

def request_prediction(url, image_bytes):
    start = time.perf_counter()
    response = requests.post(
        url,
        files={"file": ("handspell.png", image_bytes, "image/png")},
        timeout=(10, 120),
    )
    response.raise_for_status()
    payload = response.json()
    return {
        **normalize_result(payload),
        "raw": payload,
        "elapsed": time.perf_counter() - start,
        "url": response.url,
    }

def accepted_letter(result, threshold):
    if result.get("error") or result["no_hand"]:
        return "?"
    score = result["confidence"]
    return "?" if score is not None and score < threshold else result["letter"]

def render_result(result, threshold):
    if result.get("error"):
        st.error(result["error"])
        return
    print(result, threshold)
    letter = accepted_letter(result, threshold)
    if result["no_hand"]:
        st.warning("No hand/sign detected. Try a clear photo of the whole hand.")
    elif letter == "?":
        st.warning("Below your display threshold. Try another photo.")
    a, b = st.columns(2)
    with a:
        st.metric("Predicted sign", result["letter"] if not result["no_hand"] else "—")
    with b:
        score = result["confidence"]
        st.metric("Model score", "—" if score is None else f"{score:.1%}")
    if result["confidence"] is not None:
        st.progress(float(result["confidence"]))
    st.caption(f"Request completed in {result['elapsed']:.2f} s")
    with st.expander("API response"):
        st.caption(result["url"])
        st.json(result["raw"])



st.markdown(
    "# <span class='accent'>Read</span> It",
    unsafe_allow_html=True,
)
st.subheader("Hand Sign Translation")

# st.divider()
# left, right = st.columns([1, 1], gap="large")


# with left:
#     st.header("Image input")
#     st.caption("Use good lighting and keep the whole hand and wrist visible.")
#     source = st.radio("Input", ["Upload image", "Take a photo"], horizontal=True)
#     upload = (st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"],
#                 key="single_upload") if source == "Upload image"
#                 else st.camera_input("Take a hand sign photo"))
#     files = [upload] if upload is not None else []

#     prepared = []
#     for file in files:
#         try:
#             image, encoded = read_image(file)
#             prepared.append({"name": file.name, "image": image, "bytes": encoded})
#         except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
#             st.error(f"Cannot read {file.name}: {exc}")

#     if prepared:
#         st.image(prepared[0]["image"], caption=prepared[0]["name"], width=420)


#     run = st.button("⚡ Translate",
#                     type="primary", disabled=not prepared or len(prepared) != len(files))
#     if run:
#         results = []
#         with st.spinner("Reading hand signs…"):
#             for item in prepared:
#                 try:
#                     result = request_prediction(API_PREDICT_ENDPOINT, item["bytes"])
#                 except (requests.RequestException, ValueError) as exc:
#                     result = {"error": f"Prediction failed: {exc}"}
#                     results.append({"name": item["name"], **result})
#         st.session_state["results"] = results

# results = st.session_state.get("results", [])

# with right:
#     st.header("Translation results")
#     if not results:
#         st.info("Choose your images and select Translate.")
#     elif results:
#         render_result(results[0], 0.0)
#         with st.expander("All API responses"):
#             st.json(results)


def main():
    configured_url = os.getenv("API_URL", "")
    if not configured_url:
        try:
            configured_url = st.secrets["API_URL"]
        except (FileNotFoundError, KeyError):
            configured_url = "http://localhost:8000"

    try:
        url = prediction_url(configured_url)
    except (ValueError, AttributeError) as exc:
        st.error(f"Invalid API_URL configuration: {exc}")
        st.stop()

    st.divider()
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.header("Image input")
        st.caption("Use good lighting and keep the whole hand and wrist visible.")
        source = st.radio("Input", ["Upload image", "Take a photo"], horizontal=True)
        upload = (st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"],
                    key="single_upload") if source == "Upload image"
                  else st.camera_input("Take a hand sign photo"))
        files = [upload] if upload is not None else []

        prepared = []
        for file in files:
            try:
                image, encoded = read_image(file)
                prepared.append({"name": file.name, "image": image, "bytes": encoded})
            except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
                st.error(f"Cannot read {file.name}: {exc}")

        if prepared:
            st.image(prepared[0]["image"], caption=prepared[0]["name"], width=420)

        run = st.button("⚡ Translate",
                        type="primary", disabled=not prepared or len(prepared) != len(files))
        if run:
            results = []
            with st.spinner("Reading hand signs…"):
                for item in prepared:
                    try:
                        result = request_prediction(url, item["bytes"])
                    except (requests.RequestException, ValueError) as exc:
                        result = {"error": f"Prediction failed: {exc}"}
                    results.append({"name": item["name"], **result})
            st.session_state["results"] = results

    results = st.session_state.get("results", [])
    with right:
        st.header("Translation results")
        if not results:
            st.info("Choose your images and select Translate.")
        else:
            render_result(results[0], 0.0)
        if results:
            with st.expander("All API responses"):
                st.json(results)


if __name__ == "__main__":
    main()
