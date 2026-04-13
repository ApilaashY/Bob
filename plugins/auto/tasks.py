from dotenv import dotenv_values
from google import genai
from google.genai import types
import os
import sys

def createFunction(name: str, module: str, desc: str, params: list[str]):
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Remove quotations from params AI mixups
    name = name.replace("'", "").replace('"', "")
    module = module.replace("'", "").replace('"', "")

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=f"Create the contents of a python file that {desc} with the function to be called named: {name} and parameters: {params}",
        config=types.GenerateContentConfig(
            system_instruction="You are a python code generator. You only output the python code. No explanations. No extra text. Just the python code. Your output should be able to be put into a python file and executed without any runtime or logical errors"
        )
    )

    try:
        os.mkdir(f"plugins/{module}")
    except:
        print("MODULE ALREADY EXISTS")

    with open(f"plugins/{module}/tasks.py", "a") as f:
        f.write(response.text)
    with open(f"plugins/{module}/functions.txt", "a") as f:
        f.write(f"{name} < {str(params)[1:-1]}: {desc}\n")
    

if __name__ == "__main__":
    createFunction("getTime", "time", "returns the exact time as a string", [])