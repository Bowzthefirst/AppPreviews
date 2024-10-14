
# main.py

import sys
import streamlit as st
from PIL import Image

# Add paths to sys.path for module discovery
sys.path.append(".")  # Current directory: app/
sys.path.append("../AppPreviews/config/")  # Relative path to config

from image_processing import overlay_screenshot_with_frame
import config

st.title("Multiple Image Placement in iPhone Frame")

# Load the iPhone frame from the configuration path
iphone_frame = Image.open(config.IPHONE_FRAME_PATH)

# Upload multiple screenshot images
uploaded_images = st.file_uploader("Upload Screenshots", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Process each uploaded screenshot
if uploaded_images:
    for idx, uploaded_image in enumerate(uploaded_images):
        input_image = Image.open(uploaded_image)
        
        # Overlay the screenshot with the iPhone frame using the configured corner radius
        final_image = overlay_screenshot_with_frame(input_image, iphone_frame, radius=config.DEFAULT_CORNER_RADIUS)
        
        # Display the final image with caption
        st.image(final_image, caption=f"Screenshot {idx + 1} with iPhone Frame Overlay", use_column_width=True)
        
        # Save the final image and provide download option for each
        output_path = f"final_image_{idx + 1}.png"
        final_image.save(output_path)
        
        with open(output_path, "rb") as file:
            st.download_button(
                label=f"Download Framed Image {idx + 1}",
                data=file,
                file_name=output_path,
                mime="image/png"
            )

