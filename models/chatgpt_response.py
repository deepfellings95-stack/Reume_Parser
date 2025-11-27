import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class chatGPTResponse:
    def __init__(self, text):
        self.text = text
        self.prompt = f"""
Extract structured resume information in JSON format.

Fields:
- name
- email
- phone
- skills (list)
- education (list)
- experience (list)

Resume:
\"\"\"{self.text}\"\"\"
IMPORTANT:
- Return ONLY valid JSON.
- Do NOT wrap the JSON in ```json``` or any code fences.
- No explanation, no text before or after.
"""

    def get_response(self):
        try:
            key = os.getenv('OPENRouter_CHATGPT_KEY')
            if not key:
                return "no key"
            
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key = key)
            
            response = client.chat.completions.create(
                model= "openai/gpt-oss-20b:free",
                messages = [{
                    'role': 'user',
                    "content": self.prompt
                    }
                            ]
                )
            return response
        except Exception as e:
            return f" error {e}" 
            









                    
