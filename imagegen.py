from names import getnames
from PIL import Image, ImageDraw, ImageFont

# thanks chatgpt

def write_text():

    listnames = getnames()
    print(listnames)
    image_size = 1024
    
    try:
        font = ImageFont.truetype("Atkinson-Hyperlegible-Regular-102.otf", size=100)
    except IOError:
        font = ImageFont.load_default()

    # Starting position for text
    
    # space between lines
    # Write each tuple on a separate line
    i=0
    print(listnames)
    for t in listnames:
        x, y = 512, 300
        print(t)
        image = Image.open('template.png')
        draw = ImageDraw.Draw(image)
        output_path = str(i)+'output_image.png'
        line_height = 100
        text = f"{t[0]}"
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (image_size - text_width) / 2
        y = (image_size - text_height) / 3

        draw.text((x, y), text, fill="black", font=font)
        text1 = f"{t[1]}"


        bbox = draw.textbbox((0, 0), text1, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (image_size - text_width) / 2
        y = (image_size - text_height) / 2

        y += line_height
        draw.text((x, y), text1, fill="black", font=font)
        image.save(output_path)
        i+=1
     # Save the image
    
    print(f"Saved image with text to {output_path}")

if __name__ == "__main__":
    write_text()




