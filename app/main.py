# main.py

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from image_processing import overlay_screenshot_with_frame
import config

def create_colored_background(width: int, height: int, color: tuple) -> Image.Image:
    return Image.new("RGBA", (width, height), color)

def place_on_background(downscaled_image: Image.Image, background: Image.Image, padding: int, text: str) -> Image.Image:
    # Calculate position for bottom-aligned image
    position = ((background.width - downscaled_image.width) // 2, 
                background.height - downscaled_image.height - padding)
    background.paste(downscaled_image, position, downscaled_image)
    
    # Draw the text above the framed image
    draw = ImageDraw.Draw(background)
    font_size = 80  # Ensure this is large enough to see any effect
    font_path = "assets/fonts/DejaVuSans-Bold.ttf"  # Adjust path if necessary
    
    try:
        # Load the custom font and verify its size
        font = ImageFont.truetype(font_path, font_size)
        st.write(f"Loaded font from: {font_path} with size: {font_size}")
    except IOError:
        # Fall back to default font (non-resizable, for troubleshooting)
        st.write("Failed to load custom font, falling back to default.")
        font = ImageFont.load_default()
    
    # Calculate text bounding box and center it horizontally with more spacing above the framed image
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Increase the spacing between the text and the framed image
    text_position = ((background.width - text_width) // 2, position[1] - text_height - 150)  # 150px gap
    draw.text(text_position, text, font=font, fill="white")
    
    return background



st.title("Enhanced Screenshot Placement with Larger Text and More Spacing")

# Load the iPhone frame from the config path
iphone_frame = Image.open(config.IPHONE_FRAME_PATH)

# Background color, padding, corner radius, and image scale adjustments
bg_color = st.color_picker("Choose a background color", "#000000")
background_color = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5)) + (255,)
padding = st.slider("Select bottom padding", min_value=0, max_value=500, value=50)
corner_radius = st.slider("Select corner radius for image", min_value=0, max_value=300, value=150)
image_scale = st.slider("Adjust image scale", min_value=1000, max_value=1300, value=1100)

# Upload multiple screenshot images
uploaded_images = st.file_uploader("Upload Screenshots", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Process each uploaded screenshot
if uploaded_images:
    # Collect text inputs for each image
    text_inputs = []
    for idx in range(len(uploaded_images)):
        text = st.text_input(f"Enter text for Image {idx + 1}", f"Sample Text {idx + 1}")
        text_inputs.append(text)
        
    for idx, uploaded_image in enumerate(uploaded_images):
        input_image = Image.open(uploaded_image)
        
        # Overlay the screenshot with the iPhone frame, using the chosen corner radius
        framed_image = overlay_screenshot_with_frame(input_image, iphone_frame, radius=corner_radius)
        
        # Adjust the size of the image to be larger before placing on the background
        aspect_ratio = framed_image.height / framed_image.width
        downscaled_size = (image_scale, int(image_scale * aspect_ratio))
        downscaled_image = framed_image.resize(downscaled_size)
        
        # Create a colored background of 1320px by 2868px
        colored_background = create_colored_background(1320, 2868, background_color)
        
        # Place the downscaled image onto the colored background, bottom-aligned with padding, and add specific text
        final_image = place_on_background(downscaled_image, colored_background, padding, text_inputs[idx])
        
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
