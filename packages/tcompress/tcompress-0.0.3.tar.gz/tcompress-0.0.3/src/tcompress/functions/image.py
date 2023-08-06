from PIL import Image
import aggdraw

transparent = (0, 0, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
fuchsia = (255, 0, 255)
green = (0, 255, 0)
aqua = (0, 255, 255)
yellow = (255, 255, 0)

def add_padding(image_path, padding_value, color):
    image = Image.open(image_path)
    top = right = bottom = left = padding_value
    width, height = image.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(image.mode, (new_width, new_height), color)
    result.paste(image, (left, top))
    result.save(image_path)
    
def round_corners(image_path, radius):
    image = Image.open(image_path)
    mask = Image.new('L', image.size)
    draw = aggdraw.Draw(mask)
    brush = aggdraw.Brush('white')
    width, height = mask.size
    draw.pieslice((0, 0, radius*2, radius*2), 90, 180, 255, brush)
    draw.pieslice((width - radius*2, 0, width, radius*2), 0, 90, None, brush)
    draw.pieslice((0, height - radius * 2, radius *
                   2, height), 180, 270, None, brush)
    draw.pieslice((width - radius * 2, height - radius *
                   2, width, height), 270, 360, None, brush)
    draw.rectangle((radius, radius, width - radius, height - radius), brush)
    draw.rectangle((radius, 0, width - radius, radius), brush)
    draw.rectangle((0, radius, radius, height-radius), brush)
    draw.rectangle((radius, height-radius, width-radius, height), brush)
    draw.rectangle((width-radius, radius, width, height-radius), brush)
    draw.flush()
    image = image.convert('RGBA')
    image.putalpha(mask)
    image.save(image_path)

def turn_to_square(image_path, color):
    image = Image.open(image_path)
    x, y = image.size
    size = max(256, x, y)
    new_image = Image.new('RGB', (size, size), color = color)
    new_image.paste(image, (int((size - x) / 2), int((size - y) / 2)))
    new_image.save(image_path)
