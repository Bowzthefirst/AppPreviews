import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from image_processing import overlay_screenshot_with_frame
import config
import base64
from io import BytesIO

def create_colored_background(width: int, height: int, color: tuple) -> Image.Image:
    return Image.new("RGBA", (width, height), color)

def place_on_background(downscaled_image: Image.Image, background: Image.Image, padding: int, text: str, text_color: tuple) -> Image.Image:
    position = ((background.width - downscaled_image.width) // 2, 
                background.height - downscaled_image.height - padding)
    background.paste(downscaled_image, position, downscaled_image)
    
    draw = ImageDraw.Draw(background)
    font_size = 80
    font_path = "assets/fonts/DejaVuSans-Bold.ttf"
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_position = ((background.width - text_width) // 2, position[1] - text_height - 150)
    draw.text(text_position, text, font=font, fill=text_color)
    
    return background

def get_image_base64(img: Image.Image) -> str:
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

st.title("Enhanced Screenshot Placement with Custom Text and Background Colors")

# Define the iPhone frame image from the config path
iphone_frame = Image.open(config.IPHONE_FRAME_PATH)

# Background color and text color pickers
bg_color = st.color_picker("Choose a background color", "#000000")
text_color = st.color_picker("Choose a text color", "#FFFFFF")

# Convert colors from hex to RGBA format
background_color = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5)) + (255,)
text_color_rgba = tuple(int(text_color[i:i+2], 16) for i in (1, 3, 5)) + (255,)

# Additional settings
padding = st.slider("Select bottom padding", min_value=0, max_value=500, value=50)
corner_radius = st.slider("Select corner radius for image", min_value=0, max_value=300, value=150)
image_scale = st.slider("Adjust image scale", min_value=1000, max_value=1400, value=1200)

uploaded_images = st.file_uploader("Upload Screenshots", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_images:
    text_inputs = []
    for idx in range(len(uploaded_images)):
        text = st.text_input(f"Enter text for Image {idx + 1}", f"Sample Text {idx + 1}")
        text_inputs.append(text)
        
    for idx, uploaded_image in enumerate(uploaded_images):
        input_image = Image.open(uploaded_image)
        
        # Use the iPhone frame image
        framed_image = overlay_screenshot_with_frame(input_image, iphone_frame, radius=corner_radius)
        
        aspect_ratio = framed_image.height / framed_image.width
        downscaled_size = (image_scale, int(image_scale * aspect_ratio))
        downscaled_image = framed_image.resize(downscaled_size)
        
        colored_background = create_colored_background(1320, 2868, background_color)
        
        final_image = place_on_background(downscaled_image, colored_background, padding, text_inputs[idx], text_color_rgba)
        
        # Resize for display and encode to base64
        display_image = final_image.resize((400, int(400 * final_image.height / final_image.width)))
        img_str = get_image_base64(display_image)
        
        # Display the image using base64 encoding in Markdown
        st.markdown(f"<div style='text-align: center;'><img src='data:image/png;base64,{img_str}' width='400'/></div>", unsafe_allow_html=True)
        
        output_path = f"final_image_{idx + 1}.png"
        final_image.save(output_path)
        
        with open(output_path, "rb") as file:
            st.download_button(
                label=f"Download Final Image {idx + 1}",
                data=file,
                file_name=output_path,
                mime="image/png"
            )
