from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import streamlit as st

from main import get_output_max, log_transform


def decode_uploaded_image(uploaded_file) -> np.ndarray | None:
    file_bytes = np.frombuffer(uploaded_file.getvalue(), dtype=np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)


def to_display_image(image: np.ndarray) -> np.ndarray:
    display_image = image

    if display_image.ndim == 3 and display_image.shape[2] == 3:
        display_image = cv2.cvtColor(display_image, cv2.COLOR_BGR2RGB)
    elif display_image.ndim == 3 and display_image.shape[2] == 4:
        display_image = cv2.cvtColor(display_image, cv2.COLOR_BGRA2RGBA)

    if display_image.dtype == np.uint8:
        return display_image

    normalized = cv2.normalize(display_image, None, 0, 255, cv2.NORM_MINMAX)
    return normalized.astype(np.uint8)


def encode_image_for_download(image: np.ndarray, suffix: str) -> bytes:
    extension = suffix.lower() if suffix else ".png"
    success, encoded = cv2.imencode(extension, image)
    if not success:
        success, encoded = cv2.imencode(".png", image)
        if not success:
            raise RuntimeError("Khong ma hoa duoc anh de tai xuong.")
    return encoded.tobytes()


st.set_page_config(page_title="Log Transform X-ray", layout="wide")
st.title("Bien doi logarit cho anh X-quang")
st.write("Cong thuc ap dung: `s = c * log(1 + r)`")

uploaded_file = st.file_uploader(
    "Chon anh de xu ly", type=["png", "jpg", "jpeg", "tif", "tiff", "bmp"]
)

if uploaded_file is None:
    st.info("Tai len mot anh de xem ket qua bien doi logarit.")
    st.stop()

image = decode_uploaded_image(uploaded_file)
if image is None:
    st.error("Khong doc duoc file anh vua tai len.")
    st.stop()

r_max = float(image.max())
output_max = get_output_max(image)
default_c = output_max / np.log1p(r_max) if r_max > 0 else 1.0
max_c = max(default_c * 3, 1.0)

st.sidebar.header("Dieu chinh tham so")
c_value = st.sidebar.slider(
    "Gia tri c",
    min_value=0.1,
    max_value=float(max_c),
    value=float(default_c),
    step=max(float(default_c) / 100, 0.1),
)

transformed, _, _ = log_transform(image, c_value=c_value)

st.sidebar.write(f"`c goi y = {default_c:.4f}`")
st.sidebar.write(f"`output_max = {output_max:.0f}`")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Anh goc")
    st.image(to_display_image(image), use_container_width=True, clamp=True)

with col2:
    st.subheader("Anh sau bien doi")
    st.image(to_display_image(transformed), use_container_width=True, clamp=True)

download_name = f"{Path(uploaded_file.name).stem}_log{Path(uploaded_file.name).suffix or '.png'}"
download_bytes = encode_image_for_download(
    transformed, Path(uploaded_file.name).suffix or ".png"
)

st.download_button(
    "Tai anh da xu ly",
    data=download_bytes,
    file_name=download_name,
    mime="application/octet-stream",
)
