from names import getnames
from PIL import Image, ImageDraw, ImageFont

# thanks chatgpt

    
def filter():
    listnames = getnames()
    i=0
    for name in listnames:
        if len(name[0]) and len(name[1]) < 19:
            write_text(name,i)
            i+=1
        else:
            print(name)
            print("could not print because it was too long")
            return
            

def write_text(text,index):

    image_size = 1024
    x, y = 512, 300
    
    try:
        font = ImageFont.truetype("Atkinson-Hyperlegible-Regular-102.otf", size=120)
    except IOError:
        font = ImageFont.load_default()
    
    image = Image.open('resources/template.png')
    draw = ImageDraw.Draw(image)
    output_path = f'output/{str(index)}output_image.png'
    line_height = 100
        
    bbox = draw.textbbox((0, 0), text[0], font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (image_size - text_width) / 2
    y = (image_size - text_height) / 3

    draw.text((x, y), text[0], fill="black", font=font)

    bbox = draw.textbbox((0, 0), text[1], font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (image_size - text_width) / 2
    y = (image_size - text_height) / 2

    y += line_height
    draw.text((x, y), text[1], fill="black", font=font)
    image.save(output_path)

if __name__ == "__main__":
    filter()
    




