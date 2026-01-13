import requests
import json


def call_render(text):
    url = "https://project-resume-parser-1.onrender.com/parse"
    try:
        response = requests.post(url, json={"text": text}, timeout=40)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
