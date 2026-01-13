import os
import json
from openai import OpenAI

class GroqResumeParser:
    def __init__(self, text, model="llama-3.3-70b-versatile"):
        self.text = text
        self.model = model
        self.prompt = f"""
Extract structured resume information in valid JSON format.
Return these fields:
- name
- email
- phone
- skills (as a list)
- education (as a list of objects with school, degree, year)
- experience (as a list of objects with company, role, duration, description)

Resume Text:
\"\"\"{self.text}\"\"\"

Rules:
- ONLY return valid JSON.
- Do NOT include any markdown formatting (like ```json).
- Ensure all escape characters are handled correctly.
- If a field is missing, return an empty string or empty list as appropriate.
"""

    def get_response(self):
        try:
            # Use Groq API Key
            key = os.getenv('GROQ_API_KEY')
            if not key:
                return {"error": "Missing Groq API Key"}
            
            # Groq is OpenAI-compatible
            client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=key,
            )
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{'role': 'user', 'content': self.prompt}],
                response_format={"type": "json_object"} # Groq supports JSON mode
            )
            
            result = response.choices[0].message.content.strip()
            
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                # Fallback: try to clean common issues
                cleaned_result = result.replace('```json', '').replace('```', '').strip()
                
                return json.loads(cleaned_result)
                
        except Exception as e:
            print(f"Error in Groq API call: {e}")
            return {"error": str(e)}

# Example of how to update the route:
"""
@upload_bp.route('/generate_result/<int:id>/<int:model_idx>')
def generate_result(id, model_idx):
    post = Post.query.get_or_404(id)
    
    # Groq models are much more reliable and have higher limits
    # You can use llama-3.3-70b-versatile or llama3-8b-8192
    groq_models = ["llama-3.3-70b-versatile", "llama3-8b-8192", "mixtral-8x7b-32768"]
    
    if model_idx >= len(groq_models):
        return "All models failed or limit reached", 400

    if not post.text:
        return 'No extraction text available', 400 

    parser = GroqResumeParser(post.text, groq_models[model_idx])
    resume_json = parser.get_response()

    if 'error' in resume_json:
        # Recursive retry with next model if one fails
        return generate_result(id=id, model_idx=model_idx + 1)

    # ... rest of your logic to save to DB ...
"""
