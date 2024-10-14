# image_processing.py

from PIL import Image, ImageDraw, ImageOps

def round_corners(image: Image.Image, radius: int) -> Image.Image:
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius=radius, fill=255)
    
    rounded_image = image.convert("RGBA")
    rounded_image.putalpha(mask)
    
    return rounded_image

def overlay_screenshot_with_frame(input_image: Image.Image, iphone_frame: Image.Image, radius: int) -> Image.Image:
    target_width = 1590  # Adjust as needed for the frame
    aspect_ratio = input_image.height / input_image.width
    upscale_size = (target_width, int(target_width * aspect_ratio))
    
    resized_image = input_image.resize(upscale_size)
    rounded_image = round_corners(resized_image, radius)
    
    background = Image.new("RGBA", iphone_frame.size)
    position = ((iphone_frame.width - upscale_size[0]) // 2, (iphone_frame.height - upscale_size[1]) // 2)
    
    background.paste(rounded_image, position, rounded_image)
    result_image = Image.alpha_composite(background, iphone_frame.convert("RGBA"))
    
    return result_image
