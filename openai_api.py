import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def extract_image_o1():
    base64_image = encode_image("image1.png")
    response = client.responses.create(
        model="o1-2024-12-17",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "extract all the details related to the coding question in the image in a nice format"},
                {"type": "input_image", "image_url": f"data:image/jpeg;base64,{base64_image}"},
            ],
        }],
    )
    print(response.output_text)
    return response.output_text

def image_to_o1():
    base64_image = encode_image("image1.png")
    response = client.responses.create(
        model="o1-2024-12-17",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "solve the coding question in this image in python"},
                {"type": "input_image", "image_url": f"data:image/jpeg;base64,{base64_image}"},
            ],
        }],
    )
    print(response.output_text)
    return response.output_text

def question_to_o3(question):
    resp = client.chat.completions.create(
        model="o3-mini-2025-01-31",
        messages=[
            {"role": "system", "content": "Solve this coding problem and provide the answer in Python."},
            {"role": "user", "content": question},
        ],
        reasoning_effort="high"
    )
    print(resp.choices[0].message.content)
    return resp.choices[0].message.content