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

    temp_image_path = f"temp{ext}"
    with open(temp_image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    import glob
    for svg_file in glob.glob("*.svg"):
        try:
            os.remove(svg_file)
        except Exception as e:
            st.warning(f"Could not delete {svg_file}: {e}")
    output_path = "output.step"

    # Remove old STEP file if it exists
    if os.path.exists(output_path):
        os.remove(output_path)

    with st.spinner("Processing image..."):
        generate_step_from_2d_cad_image(temp_image_path, output_path, model_type=args.model_type)

    st.success("3D CAD data has been successfully generated.")

    # Download button
    try:
        with open(output_path, "rb") as f:
            st.download_button("Download STEP File", f, file_name="output.step", mime="application/octet-stream")
    except FileNotFoundError:
        st.error("The output.step file was not found. Please try again.")
    else:
        st.write("No image uploaded.")
