import argparse
import os

import streamlit as st
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
from cad3dify import generate_step_from_2d_cad_image


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_type", type=str, default="gpt")
    return parser.parse_args()


args = parse_args()

st.title("2D Drawing to 3D CAD")

uploaded_file = st.sidebar.file_uploader("Select an image file", type=["jpg", "jpeg", "png"])

# Display the image if uploaded
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    ext = os.path.splitext(uploaded_file.name)[1]
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("Image size: ", image.size)
    with open(f"temp.{ext}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    with st.spinner("Processing image..."):
        generate_step_from_2d_cad_image(
            f"temp.{ext}", "output.step", model_type=args.model_type
        )
    st.success("3D CAD data has been successfully generated.")
else:
    st.write("No image uploaded.")
