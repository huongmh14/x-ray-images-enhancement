from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import streamlit as st

from main import get_output_max, log_transform


def decode_uploaded_image(uploaded_file) -> np.ndarray | None:
    du_lieu_tep = np.frombuffer(uploaded_file.getvalue(), dtype=np.uint8)
    return cv2.imdecode(du_lieu_tep, cv2.IMREAD_UNCHANGED)


def to_display_image(image: np.ndarray) -> np.ndarray:
    anh_hien_thi = image

    if anh_hien_thi.ndim == 3 and anh_hien_thi.shape[2] == 3:
        anh_hien_thi = cv2.cvtColor(anh_hien_thi, cv2.COLOR_BGR2RGB)
    elif anh_hien_thi.ndim == 3 and anh_hien_thi.shape[2] == 4:
        anh_hien_thi = cv2.cvtColor(anh_hien_thi, cv2.COLOR_BGRA2RGBA)

    if anh_hien_thi.dtype == np.uint8:
        return anh_hien_thi

    anh_chuan_hoa = cv2.normalize(anh_hien_thi, None, 0, 255, cv2.NORM_MINMAX)
    return anh_chuan_hoa.astype(np.uint8)


def encode_image_for_download(image: np.ndarray, suffix: str) -> bytes:
    phan_mo_rong = suffix.lower() if suffix else ".png"
    thanh_cong, anh_da_ma_hoa = cv2.imencode(phan_mo_rong, image)
    if not thanh_cong:
        thanh_cong, anh_da_ma_hoa = cv2.imencode(".png", image)
        if not thanh_cong:
            raise RuntimeError("Khong ma hoa duoc anh de tai xuong.")
    return anh_da_ma_hoa.tobytes()


st.set_page_config(page_title="Log Transform X-ray", layout="wide")
st.title("Bien doi logarit cho anh X-quang")
st.write("Cong thuc ap dung: `s = c * log(1 + r)`")

tep_tai_len = st.file_uploader(
    "Chon anh de xu ly", type=["png", "jpg", "jpeg", "tif", "tiff", "bmp"]
)

if tep_tai_len is None:
    st.info("Tai len mot anh de xem ket qua bien doi logarit.")
    st.stop()

anh = decode_uploaded_image(tep_tai_len)
if anh is None:
    st.error("Khong doc duoc file anh vua tai len.")
    st.stop()

gia_tri_anh_lon_nhat = float(anh.max())
gia_tri_dau_ra_lon_nhat = get_output_max(anh)
gia_tri_c_mac_dinh = (
    gia_tri_dau_ra_lon_nhat / np.log1p(gia_tri_anh_lon_nhat)
    if gia_tri_anh_lon_nhat > 0
    else 1.0
)
gia_tri_c_toi_da = max(gia_tri_c_mac_dinh * 3, 1.0)

st.sidebar.header("Dieu chinh tham so")
gia_tri_c = st.sidebar.slider(
    "Gia tri c",
    min_value=0.1,
    max_value=float(gia_tri_c_toi_da),
    value=float(gia_tri_c_mac_dinh),
    step=max(float(gia_tri_c_mac_dinh) / 100, 0.1),
)

anh_sau_bien_doi, _, _ = log_transform(anh, c_value=gia_tri_c)

st.sidebar.write(f"`c goi y = {gia_tri_c_mac_dinh:.4f}`")
st.sidebar.write(f"`output_max = {gia_tri_dau_ra_lon_nhat:.0f}`")

cot_1, cot_2 = st.columns(2)

with cot_1:
    st.subheader("Anh goc")
    st.image(to_display_image(anh), use_container_width=True, clamp=True)

with cot_2:
    st.subheader("Anh sau bien doi")
    st.image(to_display_image(anh_sau_bien_doi), use_container_width=True, clamp=True)

ten_tep_tai_xuong = (
    f"{Path(tep_tai_len.name).stem}_log{Path(tep_tai_len.name).suffix or '.png'}"
)
du_lieu_tai_xuong = encode_image_for_download(
    anh_sau_bien_doi, Path(tep_tai_len.name).suffix or ".png"
)

st.download_button(
    "Tai anh da xu ly",
    data=du_lieu_tai_xuong,
    file_name=ten_tep_tai_xuong,
    mime="application/octet-stream",
)
