from dotenv import load_dotenv
from openai import OpenAI
import os
import base64

load_dotenv()
client = OpenAI()


def general_response(voice_command):

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": voice_command,
            },
        ],
    )

    return completion.choices[0].message


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
                        "text": "Please describe the image.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )

    return response.choices[0].message.content


def image_response():
    recent_image_path = os.listdir("images")[-1]
    image_path = os.path.join("images", recent_image_path)
    return describe_image(image_path)
