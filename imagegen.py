from names import getnames
from PIL import Image, ImageDraw, ImageFont

# thanks chatgpt

def write_text():

    listnames = getnames()
    print(listnames)
    
    
    try:
        font = ImageFont.truetype("Atkinson-Hyperlegible-Regular-102.otf", size=100)
    except IOError:
        font = ImageFont.load_default()

    # Starting position for text
    x, y = 512, 300
    # space between lines
    
    # Write each tuple on a separate line
    i=0
    print(listnames)
    for t in listnames:
        print(t)
        image = Image.open('template.png')
        draw = ImageDraw.Draw(image)
        output_path = str(i)+'output_image.png'
        line_height = 100
        text = f"{t[0]}"
        text1 = f"{t[1]}"
        draw.text((x, y), text, fill="black", font=font)
        y += line_height
        draw.text((x, y), text1, fill="black", font=font)
        y += line_height
        image.save(output_path)
        i+=1
     # Save the image
    
    print(f"Saved image with text to {output_path}")

if __name__ == "__main__":
    write_text()




