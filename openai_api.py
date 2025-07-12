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
    input_items = [
        {"type": "input_text", "text": "extract all the details related to the coding question in the images in a nice format"}
    ]

    image_paths = []

    for filename in sorted(os.listdir("query")):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join("query", filename)
            image_paths.append(path)
            base64_image = encode_image(path)
            input_items.append({
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{base64_image}"
            })

    response = client.responses.create(
        model="o1-2024-12-17",
        input=[{
            "role": "user",
            "content": input_items
        }],
    )

    print(response.output_text)

    # Cleanup all images after success
    for path in image_paths:
        try:
            os.remove(path)
        except Exception as e:
            print(f"⚠️ Failed to delete {path}: {e}")

    return response.output_text

def image_to_o1(text):
    input_items = [
        {"type": "input_text", "text": text}
    ]

    # Iterate over all image files in the query directory
    for filename in sorted(os.listdir("query")):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join("query", filename)
            base64_image = encode_image(path)
            input_items.append({
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{base64_image}"
            })

    response = client.responses.create(
        model="o1-2024-12-17",
        input=[{
            "role": "user",
            "content": input_items
        }],
    )

    print(response.output_text)
    return response.output_text

def question_to_o3(question, model_name):
    # Prepare base messages
    messages = [
        {"role": "system", "content": "Solve this coding problem and provide the answer in Python covering all test cases keeping in mind the constraints also provide explanation of you approach in short about 10 lines before the code using comments."},
        {"role": "user", "content": question},
    ]

    kwargs = {
        "model": model_name,
        "messages": messages,
    }

    # Apply reasoning_effort only for o3-mini or o1/o3 series
    if model_name.startswith("o3"):
        kwargs["reasoning_effort"] = "high"

    response = client.chat.completions.create(**kwargs)
    answer = response.choices[0].message.content
    print(answer)
    return answer