from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
# i forgot this part and it didn't work lol

# load gemini AI model
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def moderate_me(text):
    """take in tuple and return if appropriate using sentiment analysis"""

    name = text[0]
    content = text[1]

    prompt = f"""
    You're an assistant that reviews messages before posting them publicly on Instagram.

    Determine if the following message is appropriate for an Instagram post.

    Respond only with "Yes" if appropriate, or "No" if not.

    Message:
    "{name} {content}"
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        ),
    )

    if response.text.strip() == "Yes":
        return text
    else:
        print("the internet is terrible, see")
        print(text)

def generate_caption(data):
    """create a nice message from the week's acceptable posts"""
    # I hate prompt 'engineering', screaming into the void
    # neither a mortal engine nor a mechanical soul

    prompt = f"""
    You're a writer who writes catchy captions for Instagram.

    Write a short caption with only emojis that will hook readers.

    Use the information provided on the following people:

    "{data}"
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        ),
    )

    return response.text.strip()

    # print("I couldn't think of anything, go write your own.")
    # return("🤖")

if __name__ == "__main__":
    naughty = ("bitch ass whore ass cunt fuck","luck be a lady he is rude and unkind")
    nice = ("Alex Alex Alex Taylor", "never have I ever seen a hotter guy")
    moderate_me(naughty)
    moderate_me(nice)
    print(generate_caption(nice))

