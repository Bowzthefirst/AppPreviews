# main.py

import streamlit as st
from PIL import Image, ImageDraw
from image_processing import overlay_screenshot_with_frame
import config

def create_colored_background(width: int, height: int, color: tuple) -> Image.Image:
    return Image.new("RGBA", (width, height), color)

def place_on_background(downscaled_image: Image.Image, background: Image.Image, padding: int) -> Image.Image:
    # Calculate the position to bottom-align the image on the background with padding
    position = ((background.width - downscaled_image.width) // 2, 
                background.height - downscaled_image.height - padding)
    
    # Paste the downscaled image onto the background
    background.paste(downscaled_image, position, downscaled_image)
    return background

st.title("Screenshot Placement on Custom Background with Padding")

# Load the iPhone frame from the config path
iphone_frame = Image.open(config.IPHONE_FRAME_PATH)

# User selects the background color (default to black)
bg_color = st.color_picker("Choose a background color", "#000000")
background_color = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5)) + (255,)  # Convert hex to RGBA

# User selects padding for the bottom
padding = st.slider("Select bottom padding", min_value=0, max_value=500, value=50)

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
        
        # Create a colored background of 1320px by 2868px
        colored_background = create_colored_background(1320, 2868, background_color)
        
        # Place the downscaled image onto the colored background, bottom-aligned with padding
        final_image = place_on_background(downscaled_image, colored_background, padding)
        
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
