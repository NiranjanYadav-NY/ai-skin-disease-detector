#install and importing dependencies/libraries
# import anthropic 
import os
import base64
import requests
from dotenv import load_dotenv

#api keys and clients

api_keys = os.environ.get("MINIMAX_API_KEY")
base_url = "https://api.minimax.io/anthropic"

client = anthropic.Anthropic(api_key=api_key. base_url=base_url)

#creating message 
folder  = os.path.dirname(__file__)
image_path = os.path.join(folder, "dummy_img.png")

with open(image_path,"rb") as file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

messages = [
    {
        "role":"user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_data,
                },
            },
            {
                "type": "text",
                "text": "Hello, what can you help me with?",
            },
        ],
    }
]

#sending messages

response = client.messages.create(
    model = "MiniMax-M3",
    max_tokens=1000,
    messages=messages,
)

#printing responses
print(response.content[0].text)