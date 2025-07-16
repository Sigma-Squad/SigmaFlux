import requests
import json
import os
import base64
import mimetypes
from dotenv import load_dotenv


load_dotenv()  # Load variables from .env

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# Function to convert local image to base64 data URL
def image_to_data_url(image_path):                                      
    mime_type, _ = mimetypes.guess_type(image_path)
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

# Local image path
def ocr_reading(image_path,n):

    data_url = image_to_data_url(image_path)

    # Print response
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "qwen/qwen2.5-vl-72b-instruct:free",
            "temperature":0,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"This is an attendance sheet,with some printed text such as s no. roll no., name, etc and signatures in the form of scribbles in the next {n} columns which represent {n} dates. Give attendance of all the dates in tabular form. Write absent if the cell is empty or has a cross mark or there is a cut mark either horizontal or slant, otherwise mark present if there is a significant scribble. Give only the table in output"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": data_url
                            }
                        }
                    ]
                }
            ]
        })
    )
    if response.ok:
        output_text = response.json()["choices"][0]["message"]["content"]

        # Save to text file
        base, ext = os.path.splitext(image_path)

        output_path = f"{base}.txt"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_text)

        print(f"✅ Output saved to '{output_path}'")
    else:
        print("Error:", response.status_code,response.text)