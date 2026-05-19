from io import BytesIO
from pathlib import Path

import cv2
import imageio.v2 as imageio
import numpy as np
import streamlit as st

from src.algorithms.medical_pipeline import EnhancementConfig, MedicalEnhancement


st.set_page_config(page_title="X-Ray Enhancement", layout="wide")
st.title("X-Ray Image Enhancement")
st.caption("Log Transform + CLAHE + Unsharp Mask")


@st.cache_data
def load_demo_image(image_path: str) -> np.ndarray:
	return imageio.imread(image_path)


def build_processor(config: EnhancementConfig) -> MedicalEnhancement:
	return MedicalEnhancement(
		filename="web_input.png",
		results_path="results/web_preview",
		config=config,
		prompt_for_missing=False,
	)


with st.sidebar:
	st.header("Parameters")
	log_gain = st.slider("Log gain c", min_value=0.1, max_value=10.0, value=4.0, step=0.1)
	clip_limit = st.slider("CLAHE clip limit", min_value=0.1, max_value=10.0, value=2.5, step=0.1)
	tile_grid_size = st.slider("CLAHE tile grid size", min_value=2, max_value=32, value=8, step=1)
	sharpen_amount = st.slider("Unsharp amount", min_value=0.0, max_value=3.0, value=0.6, step=0.1)

	st.header("Input")
	uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "tif", "tiff", "bmp"])
	demo_images = sorted(str(path.name) for path in Path("images").glob("*") if path.is_file())
	selected_demo = st.selectbox("Or choose a demo image", options=["None"] + demo_images, index=0)


config = EnhancementConfig(
	log_gain=log_gain,
	clip_limit=clip_limit,
	tile_grid_size=tile_grid_size,
	sharpen_amount=sharpen_amount,
)

image = None
image_name = "uploaded"

if uploaded_file is not None:
	image = imageio.imread(BytesIO(uploaded_file.getvalue()))
	image_name = Path(uploaded_file.name).stem
elif selected_demo != "None":
	image = load_demo_image(str(Path("images") / selected_demo))
	image_name = Path(selected_demo).stem

if image is None:
	st.info("Upload an image or choose a demo image from the sidebar.")
	st.stop()

processor = build_processor(config)
processor.filename = f"{image_name}.png"
result = processor.run_on_image(image, export_outputs=False)

col1, col2 = st.columns(2)
with col1:
	st.subheader("Original")
	st.image(result["original"], clamp=True, use_container_width=True)
with col2:
	st.subheader("Enhanced")
	st.image(result["enhanced"], clamp=True, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
	st.subheader("Log Transform")
	st.image(result["log"], clamp=True, use_container_width=True)
with col4:
	st.subheader("CLAHE")
	st.image(result["clahe"], clamp=True, use_container_width=True)

st.metric("Runtime", f"{result['runtime']:.4f}s")

success, encoded = cv2.imencode(".png", result["enhanced"])
if not success:
	st.error("Failed to encode the enhanced image as PNG.")
	st.stop()

enhanced_bytes = encoded.tobytes()
st.download_button(
	"Download Enhanced PNG",
	data=enhanced_bytes,
	file_name=f"{image_name}_enhanced.png",
	mime="image/png",
)
