from dotenv import load_dotenv
import pytesseract
from PIL import Image
import requests
import os
import json

load_dotenv()

class imageParser:
    def __init__(self , filename):
        self.filename = filename
        
    
    def extract_all_text(self):
        
        try:
            img = Image.open(filename)
            text = pytesseract.image_to_string(img) + " TESSERAAAAACT TEXT"

            
            if text.isempty: 
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
            
                
            else:
                return text.strip()
        except Exception as e:
            pass
            
                    
        
    
