import requests
import json
import os
import base64
import mimetypes
import cv2
from dotenv import load_dotenv


load_dotenv()  # Load variables from .env

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# Function to convert local image to base64 data URL
def image_to_data_url(uploaded_image,file_name):                                      
    mime_type, _ = mimetypes.guess_type(file_name)
    ext = mimetypes.guess_extension(mime_type).lower()
    success, buffer = cv2.imencode(ext,uploaded_image)
    if not success:
        raise ValueError(f'Failed to encode image as {ext}')
    encoded = base64.b64encode(buffer).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

# Local image path
def ocr_reading(uploaded_image,n,file_name):

    data_url = image_to_data_url(uploaded_image,file_name)

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

        return output_text
        
    else:
        return ""