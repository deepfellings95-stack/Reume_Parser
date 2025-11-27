from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

class imageParser:
    def __init__(self , filename):
        self.filename = filename
        
    
    def extract_all_text(self):
        
        try:
            key = os.getenv('OCRSpace_API_KEY')
            if not key:
                return "no API KEY"
            payload = {
                'isOverlayRequired': False,
                'apikey': key
                }
            with open(self.filename, 'rb') as f:
                r = requests.post('https://api.ocr.space/parse/image',
                                  files = {self.filename: f},
                                  data = payload,
                                  )
            return json.loads(r.content.decode())

        except Exception as e:
            return f"not text extracted {e}"
        
