from names import getnames
from PIL import Image, ImageDraw, ImageFont

# thanks chatgpt

def wrap_text(text, max_length=18):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        # Check if adding the next word would exceed the max length
        if len(current_line) + len(word) + (1 if current_line else 0) <= max_length:
            if current_line:
                current_line += " "
            current_line += word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return '\n'.join(lines)

def filter():
    """this prevents too long responses from being generated"""
    listnames = getnames()
    i=0
    for name in listnames:
        if len(name[0]) and len(name[1]) < 19:
            write_text(name,i)
            i+=1
        elif len(name[0]) < 19:
            new = []
            new.append(name[0])
            new.append(wrap_text(name[1]))
            write_text(new,i)
            i+=1
        else:
            print(name)
            print("could not print because it was too long")
            

def write_text(text,index, input_path):
    """this creates the image, great function naming"""

    image_size = 1024
    x, y = 512, 200
    
    try:
        font = ImageFont.truetype("Atkinson-Hyperlegible-Regular-102.otf", size=150)
    except IOError:
        font = ImageFont.load_default()
    
    image = Image.open(input_path)
    draw = ImageDraw.Draw(image)
    output_path = f'output/{str(index)}output_image.png'
    line_height = 150
        
    bbox = draw.textbbox((0, 0), text[0], font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (image_size - text_width) / 2
    y = (image_size - text_height) / 3

    draw.text((x, y), text[0], fill="#181818", font=font)

    bbox = draw.textbbox((0, 0), text[1], font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (image_size - text_width) / 2
    y = (image_size - text_height) / 2

    y += line_height
    print(text[1])
    draw.multiline_text((x, y), text[1], fill="#181818", font=font, spacing=4)
    image.save(output_path)

if __name__ == "__main__":
    # print("hi")
    # import os

    # stuff_dir = os.path.join('resources', 'square')
    # filenames = os.listdir(stuff_dir)
    # temp = "["
    # for filename in filenames:
    #     # print(f"{filename},")
    #     temp += f'"{filename}",'
    # temp += "]"
    # print(temp)
    filter()
    