import os
import sys
import importlib
from time import sleep

from names import getnames



def main():

    # 1. Get the names (already done)
    # listnames = getnames()
    listnames = [('testing', 'testing'), ('Hello', 'World'), ('&Hacks', 'so amazing'), ('1234567891234567891', '1234567891234567891'), ('12345678912345678', '12345678912345678'), ('123456789123456789', '123456789123456789\n123456789123456789\n123456789123456789\n123456789123456789'), ('Your Mom', 'Your mom!'), ('Shawty', 'Shawty you so fine bae'), ('François Hollande 🤨', '🏋🏻\u200d♀️🤸🏾\u200d♀️🧘🏽\u200d♀️  🏂🤸🏾\u200d♀️🤾🏿\u200d♀️🤼\u200d♀️🤾🏿\u200d♀️🤼\u200d♀️🤼\u200d♀️🤼🤾🏿\u200d♀️🤼\u200d♂️'), ('Homer         Simpson', "I'm calling out from Springfield, I'm calling out from Simpsons' world."), ('&hacks', 'I love it here!'), ('my ac unit', 'botetourt would be hell without you bestie')]
    print("Names from database:", listnames)

    # 2. Generate an image with that data (use first name as example)
    from imagegen import write_text
    if not listnames:
        print("No names found.")
        return
    
    from imagetest import create_image
    from imagegen import wrap_text

    image_index = 20
    for name in listnames:  # (name, message)

        if len(name[0]) and len(name[1]) < 19:
            create_image()
            sleep(1)
            write_text(name, image_index, "final_layered_border_image.png")
            image_path = f"output/{image_index}output_image.png"
            image_index += 1
        elif len(name[0]) < 19:
            new = []
            new.append(name[0])
            new.append(wrap_text(name[1]))
            
            create_image()
            sleep(1)
            write_text(new, image_index, "final_layered_border_image.png")
            image_path = f"output/{image_index}output_image.png"
            image_index += 1
        else:
            print(name)
            print("could not print because it was too long")


    # # 3. Call gemini to add a caption
    # from gemini import generate_caption
    # caption = generate_caption(text)
    # print("Generated caption:", caption)

        caption = "WM Crusher"

    # 4. Post the image
    # from post import login_user, post_image
    # cl = login_user()
    # post_image(cl, image_path, caption)
    # print("Image posted!")


if __name__ == "__main__":
    main()