import os
import base64
import logging
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def general_response(voice_command):

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant called Jarvis. Your answers are short and concise.",
            },
            {
                "role": "user",
                "content": voice_command,
            },
        ],
        max_tokens=64,
    )
    general_response = completion.choices[0].message.content
    logging.info(completion.choices[0].message.content)
    return general_response


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def describe_image(image_path):
    # Getting the base64 string
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please describe the image. Your answers are short and concise.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=128,
    )
    image_description = response.choices[0].message.content
    logging.info(image_description)
    return image_description


def image_response():
    recent_image_path = os.listdir("images")[-1]
    image_path = os.path.join("images", recent_image_path)
    return describe_image(image_path)
