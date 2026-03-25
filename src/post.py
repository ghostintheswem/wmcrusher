from instagrapi import Client
import os
import json
from time import sleep
from dotenv import load_dotenv
from gemini import generate_caption

load_dotenv()

# Seconds to wait between posts to avoid Instagram rate-limiting.
# Instagram's unofficial safe window is ~60s between uploads.
POST_INTERVAL_SECONDS = 60


def login_user() -> Client:
    """Log into Instagram using credentials from .env file."""
    cl = Client()
    user = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    if not user or not password:
        raise EnvironmentError(
            "INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD must be set in your .env file."
        )

    cl.login(user, password)
    print(f"Logged in as @{user}")
    return cl


def post_image(cl: Client, image_path: str, caption: str):
    """Upload a single image with a caption."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    cl.photo_upload(path=image_path, caption=caption)
    print(f"  ✓ Posted: {image_path}")


def post_all(image_paths: list[str], caption: str, interval: int = POST_INTERVAL_SECONDS):
    """
    Log in once and post a list of images with the same caption,
    waiting `interval` seconds between each post.
    """
    cl = login_user()
    for i, path in enumerate(image_paths):
        print(f"Posting {i+1}/{len(image_paths)}: {path}")
        try:
            post_image(cl, path, caption)
        except Exception as e:
            print(f"  ✗ Failed to post {path}: {e}")
            continue

        if i < len(image_paths) - 1:
            print(f"  Waiting {interval}s before next post...")
            sleep(interval)

    print("All done posting.")


# ── Standalone usage ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Post images to Instagram")
    parser.add_argument(
        "--folder", default="output",
        help="Folder containing output images (default: output/)"
    )
    parser.add_argument(
        "--caption", default=None,
        help="Caption override. If omitted, Gemini generates one from data.json."
    )
    parser.add_argument(
        "--interval", type=int, default=POST_INTERVAL_SECONDS,
        help=f"Seconds between posts (default: {POST_INTERVAL_SECONDS})"
    )
    args = parser.parse_args()

    # Collect images
    image_paths = sorted([
        os.path.join(args.folder, f)
        for f in os.listdir(args.folder)
        if f.endswith(".png")
    ])

    if not image_paths:
        print(f"No .png files found in {args.folder}/")
        exit(1)

    # Caption
    if args.caption:
        caption = args.caption
    else:
        with open("./data.json", "r") as f:
            data = [tuple(item) for item in json.load(f)]
        caption = generate_caption(data)
        print(f"Generated caption: {caption}")

    post_all(image_paths, caption, interval=args.interval)
