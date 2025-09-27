from instagrapi import Client
from datetime import datetime, timedelta
import os
import schedule

def login_user():
    cl = Client()
    cl.login("wm_.crushes", "hackerhacker1")
    print("Successfully logged in")
    return cl

def post_image(cl, image_path, caption):
    cl.photo_upload(path=image_path, caption=caption)
    print(f"Posted image: {image_path}")

def generate_daily_schedule(image_folder, start_time):
    images = os.listdir(image_folder)
    schedule_times = []
    current_time = start_time
    for _ in images:
        schedule_times.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=60)  # Post every hour
        if current_time.day != start_time.day:
            break
    return schedule_times

def schedule_and_post():
    cl = login_user()
    image_folder = 'output'
    images = os.listdir(image_folder)
    if images:
        image = images[0]
        caption = os.path.splitext(image)[0] + "\n #💚"
        image_path = os.path.join(image_folder, image)
        post_image(cl, image_path, caption)
        os.remove(image_path)
        logger.info(f"Posted and removed image: {image_path}")
        return True
    else:
        logger.info("No images left to post")
        return False

if __name__ == "__main__":
    cl = login_user()
    image_path="output/0output_image.png"
    caption="this is our test!"
    post_image(cl, image_path, caption)
    print("test")
