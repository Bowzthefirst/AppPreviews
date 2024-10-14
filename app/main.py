# main.py

import streamlit as st
from PIL import Image, ImageOps, ImageDraw
from image_processing import overlay_screenshot_with_frame
import config

def create_black_background(width: int, height: int) -> Image.Image:
    return Image.new("RGBA", (width, height), (0, 0, 0, 255))

def place_on_background(downscaled_image: Image.Image, background: Image.Image) -> Image.Image:
    # Calculate the position to bottom-align the image on the background
    position = ((background.width - downscaled_image.width) // 2, 
                background.height - downscaled_image.height)
    
    # Paste the downscaled image onto the black background
    background.paste(downscaled_image, position, downscaled_image)
    return background

st.title("Screenshot Placement on Custom Background")

# Load the iPhone frame from the config path
iphone_frame = Image.open(config.IPHONE_FRAME_PATH)

# Upload multiple screenshot images
uploaded_images = st.file_uploader("Upload Screenshots", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Process each uploaded screenshot
if uploaded_images:
    for idx, uploaded_image in enumerate(uploaded_images):
        input_image = Image.open(uploaded_image)
        
        # Overlay the screenshot with the iPhone frame
        framed_image = overlay_screenshot_with_frame(input_image, iphone_frame, radius=config.DEFAULT_CORNER_RADIUS)
        
        # Downscale the framed image to fit within the black background width
        target_width = 1000  # Adjusted width for the iPhone framed image
        aspect_ratio = framed_image.height / framed_image.width
        downscaled_size = (target_width, int(target_width * aspect_ratio))
        downscaled_image = framed_image.resize(downscaled_size)
        
        # Create a black background of 1320px by 2868px
        black_background = create_black_background(1320, 2868)
        
        # Place the downscaled image onto the black background, bottom-aligned
        final_image = place_on_background(downscaled_image, black_background)
        
        # Display the final image with caption
        st.image(final_image, caption=f"Final Image {idx + 1}", use_column_width=True)
        
        # Save the final image and provide download option for each
        output_path = f"final_image_{idx + 1}.png"
        final_image.save(output_path)
        
        with open(output_path, "rb") as file:
            st.download_button(
                label=f"Download Final Image {idx + 1}",
                data=file,
                file_name=output_path,
                mime="image/png"
            )
