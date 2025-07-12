from google import genai
from dotenv import load_dotenv
from google.genai import types
load_dotenv()
client = genai.Client()

ans_gemini =""

def gemini(question):
    global ans_gemini
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=question,
    config=types.GenerateContentConfig(
        system_instruction=[
            "Solve this coding question and answer in Python.",
            "Provide explanation of your approach before the code.",
        ]
    )
    )
    return response.text
    print(response.text)