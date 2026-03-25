# wmcrusher
automated social media posts | &hacks 2025

**Form:** https://docs.google.com/forms/d/e/1FAIpQLScCU2vwsfns_G5GQcf_RVkPuQhYKLJgoQEaLU7uKF6UZJymRQ/viewform  
**Instagram:** https://www.instagram.com/wm_.crushes/

---

## How it works

Someone fills out the Google Form → responses save to a Google Sheet → the pipeline fetches, moderates, and turns them into styled Instagram images.

### Full pipeline

1. **Fetch** — `responses.py` authenticates with Google Drive using a saved `credentials.json` and downloads the form responses as a spreadsheet. A `last_seen.json` checkpoint ensures only new responses are fetched on each run, so you never reprocess old entries or hit rate limits.

2. **Moderate** — each `(name, message)` pair is sent to Gemini 2.0 Flash one at a time. The model returns "Yes" or "No" — yes if the post is appropriate for Instagram, no if it's vulgar or mean. Rejected entries are printed and dropped. Approved entries are saved to `data.json`.

3. **Approve** — an interactive review step prints each approved entry and prompts `y/n` before any images are generated. This is the human-in-the-loop check on top of AI moderation. Bypass with `--skip-review` for automated runs.

4. **Background** — `backgrounds.py` composites a fresh background for each post from three layers of assets in `resources/`: a square photo, a paper texture on top, and 3–5 random decoration PNGs scattered around the border at 8 corner/midpoint positions. Saved as `final_layered_border_image.png`.

5. **Text** — `printimage.py` draws the name and message onto the background using Atkinson Hyperlegible at size 110. The name goes in the upper third, the message is centered below. Long messages are wrapped automatically. Entries where the name itself exceeds 16 characters are skipped — they won't fit. Output goes to `output/{index}output_image.png`.

6. **Caption** — the full batch of approved entries is sent to Gemini together to generate one short poetic Instagram caption with at least 5 emojis.

7. **Post** — `post.py` logs into Instagram via `instagrapi`, posts each image with the generated caption, and waits 60 seconds between posts to respect rate limits. Auto-posting is currently commented out in `MAIN.py` — run manually via `python post.py` or uncomment the block when ready.

---

## Setup

1. Install dependencies:
   ```
   pip install pillow pandas instagrapi pydrive python-dotenv google-generativeai
   ```

2. Create a `.env` file:
   ```
   INSTAGRAM_USERNAME=your_username
   INSTAGRAM_PASSWORD=your_password
   GEMINI_API_KEY=your_key
   ```

3. Place `credentials.json` (Google OAuth) in the project root. On first run it will open a browser to authenticate and save the token.

4. Place `Atkinson-Hyperlegible-Regular-102.otf` in the project root.

5. Populate `resources/` with:
   - `resources/square/background0.jpg` … `background25.jpg`
   - `resources/paper/paper0.png` … `paper42.png`
   - `resources/stuff/decoration0.png` … `decoration207.png`

6. Create an `output/` directory.

---

## Usage

**Full pipeline (recommended):**
```bash
python MAIN.py
```

**Skip the interactive approval step:**
```bash
python MAIN.py --skip-review
```

**Regenerate images without hitting the Google API:**
```bash
python MAIN.py --no-fetch
```

**Post images manually after generating them:**
```bash
python post.py --folder output
```

---

## Project structure

```
wmcrusher/
├── MAIN.py           # Runs the full pipeline
├── responses.py      # Fetches form responses from Google Drive
├── names.py          # Orchestrates fetch + moderation, saves data.json
├── gemini.py         # Gemini moderation and caption generation
├── backgrounds.py    # Composites layered background images
├── printimage.py     # Renders name + message text onto backgrounds
├── post.py           # Posts images to Instagram
├── data.json         # Approved entries from last run (auto-generated)
├── last_seen.json    # Timestamp checkpoint (auto-generated)
├── credentials.json  # Google OAuth token (do not commit)
├── .env              # Instagram + Gemini credentials (do not commit)
└── resources/
    ├── square/       # Background photos (background0.jpg … background25.jpg)
    ├── paper/        # Paper texture PNGs (paper0.png … paper42.png)
    └── stuff/        # Decoration PNGs (decoration0.png … decoration207.png)
```

---

## To do

- [ ] Fix formatting of images to match standard of previous account
- [ ] GitHub Pages publishing + RSS feed
- [ ] Finish Instagram API uploading (uncomment post block in MAIN.py)
- [ ] Find original account author — did we reinvent the wheel?
- [ ] Procedurally generate backgrounds
- [ ] AI-generated backgrounds
- [x] Gemini AI moderator
- [x] Only fetch new responses (last_seen.json checkpoint)
