import os
import json
from time import sleep
from names import getnames
from backgrounds import create_image
from printimage import wrap_text, write_text
from gemini import generate_caption
# from post import login_user, post_image  # uncomment to enable auto-posting

DATA_FILE = "./data.json"
OUTPUT_DIR = "output"
IMAGE_START_INDEX = 0

# ── Helpers ──────────────────────────────────────────────────────────────────

def load_existing_data() -> list[tuple]:
    """Load previously moderated data without hitting the API again."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return [tuple(item) for item in json.load(f)]
    return []


def fits_on_one_line(text: str, limit: int = 16) -> bool:
    return len(text) < limit


def prepare_entry(name: tuple) -> tuple | None:
    """
    Returns a (display_name, display_message) tuple ready for rendering,
    or None if the entry is too long to use at all.
    """
    display_name, message = name[0], name[1]

    if fits_on_one_line(display_name) and fits_on_one_line(message):
        return (display_name, message)
    elif fits_on_one_line(display_name):
        return (display_name, wrap_text(message))
    else:
        print(f"Skipping — name too long: {display_name!r}")
        return None


def review_and_approve(entries: list[tuple]) -> list[tuple]:
    """
    Simple interactive approval step.
    Prints each entry and asks the operator to approve (y) or skip (n).
    Returns only approved entries.

    Set the SKIP_REVIEW env var to '1' to bypass (e.g. for automated runs).
    """
    if os.getenv("SKIP_REVIEW") == "1":
        print("SKIP_REVIEW=1 — skipping approval step.")
        return entries

    approved = []
    print("\n── Approval Review ─────────────────────────────")
    for i, entry in enumerate(entries):
        print(f"\n[{i+1}/{len(entries)}]  Name: {entry[0]!r}  |  Message: {entry[1]!r}")
        choice = input("  Approve? [y/n/q to quit]: ").strip().lower()
        if choice == "q":
            print("Quitting review early.")
            break
        if choice == "y":
            approved.append(entry)
    print(f"\n{len(approved)}/{len(entries)} entries approved.\n")
    return approved


# ── Main pipeline ─────────────────────────────────────────────────────────────

def main(fetch_new: bool = True):
    """
    Full pipeline:
      1. Fetch + moderate new responses  (or load cached data.json)
      2. Approval review
      3. Generate one image per approved entry
      4. Generate a single Gemini caption for the batch
      5. (Optional) Post all images to Instagram
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ── 1. Fetch / load ──────────────────────────────────────────────────────
    if fetch_new:
        listnames = getnames(only_new=True)
    else:
        print("Loading cached data.json (no API call).")
        listnames = load_existing_data()

    if not listnames:
        print("Nothing to post. Exiting.")
        return

    print(f"Found {len(listnames)} entries after moderation.")

    # ── 2. Approval ──────────────────────────────────────────────────────────
    approved = review_and_approve(listnames)
    if not approved:
        print("No entries approved. Exiting.")
        return

    # ── 3. Image generation ───────────────────────────────────────────────────
    generated_paths = []
    for idx, name in enumerate(approved, start=IMAGE_START_INDEX):
        entry = prepare_entry(name)
        if entry is None:
            continue

        create_image()
        sleep(0.5)  # let the file system settle
        write_text(entry, idx, "final_layered_border_image.png")

        image_path = f"{OUTPUT_DIR}/{idx}output_image.png"
        generated_paths.append((image_path, entry))
        print(f"Generated: {image_path}")

    if not generated_paths:
        print("No images were generated. Exiting.")
        return

    # ── 4. Caption ────────────────────────────────────────────────────────────
    caption = generate_caption(approved)
    print(f"\nGenerated caption:\n  {caption}\n")

    # ── 5. Post ───────────────────────────────────────────────────────────────
    # Uncomment the block below once you're ready to enable auto-posting.
    #
    # cl = login_user()
    # for image_path, entry in generated_paths:
    #     post_image(cl, image_path, caption)
    #     print(f"Posted: {image_path}")
    #     sleep(60)  # Instagram rate-limit buffer between posts

    print(f"Done! {len(generated_paths)} image(s) ready in ./{OUTPUT_DIR}/")
    print("Auto-posting is disabled. Uncomment the post block in MAIN.py to enable it.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="wmcrusher pipeline")
    parser.add_argument(
        "--no-fetch", action="store_true",
        help="Skip API call and use cached data.json instead"
    )
    parser.add_argument(
        "--skip-review", action="store_true",
        help="Bypass the interactive approval step"
    )
    args = parser.parse_args()

    if args.skip_review:
        os.environ["SKIP_REVIEW"] = "1"

    main(fetch_new=not args.no_fetch)
