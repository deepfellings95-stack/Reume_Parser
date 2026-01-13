import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import ast

load_dotenv()

class chatGPTResponse:
    def __init__(self, text, model):
        self.text = text
        self.model = model
        self.prompt = f"""
Extract structured resume information in valid JSON format.

Return these fields:
- name
- email
- phone
- skills
- education 
- experience

Resume Text:
\"\"\"{self.text}\"\"\"

Rules:
- ONLY return JSON — no description.
- In json Replace \n with blank space.
- key or values should not be in single quotes.
- Handle Escape characters well.
- Pure json valid data.
- NO code block formatting.
- Phone/email optional — return empty if missing.
"""

    def get_response(self):
        try:
            #key = os.getenv('OPENRouter_CHATGPT_KEY')
            key = os.getenv('OPENRouter_CHATGPT_KEY2')
            if not key:
                return {"error": "Missing API Key"}
            
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=key,
            )

            response = client.chat.completions.create(
                model=self.model,     #"openai/gpt-oss-20b:free",
                messages=[{
                    'role': 'user',
                    'content': self.prompt
                }]
            )
            
            result = response.choices[0].message.content.strip()
            # Convert result to dict if valid JSON
            try:
                print(result.replace('\n', ''))
                return json.loads(result.replace('\n',''))
            except:
                # In case model returns invalid JSON
                return {"raw_response": result, "error": "Invalid JSON returned"}

        except Exception as e:
            print(e)
            return {"error": str(e)}
