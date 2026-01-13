from dotenv import load_dotenv
import pytesseract
from PIL import Image
import requests
import os
import json

load_dotenv()

class imageParser:
    def __init__(self, filename):
        self.filename = filename

    def extract_all_text(self):
        try:
            # Open the image and extract text using pytesseract
            img = Image.open(self.filename)
            text = pytesseract.image_to_string(img).strip()

            if not text:  # if pytesseract fails to extract text
                key = os.getenv('OCRSpace_API_KEY')
                if not key:
                    return {"error": "no API KEY"}

                payload = {
                    'isOverlayRequired': False,
                    'apikey': key
                }

                with open(self.filename, 'rb') as f:
                    r = requests.post(
                        'https://api.ocr.space/parse/image',
                        files={'file': f},
                        data=payload
                    )

                # Decode JSON response
                return r.json()

            else:
                return text + "TESSERACT PARSED2"

        except Exception as e:
            return {"error": str(e)}
