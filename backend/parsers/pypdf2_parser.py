import PyPDF2
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from parsers.image_parser2 import imageParser
import os

class pdfParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.reader = None

    def extract_all_text(self):
        full_text = ''
        try:
            os.makedirs('uploads', exist_ok=True)
            pages = convert_from_path(self.filepath)
            
            for i, page in enumerate(pages):
           
                page.save(self.filepath, "PNG")
                print(self.filepath)
                
                
                nml_text = imageParser(self.filepath)
                nml_text = nml_text.extract_all_text()
                
                full_text += nml_text.strip()
            if not full_text:
                with open(self.filepath, 'rb') as f:
                    self.reader = PdfReader(f)
                    pages = self.reader.pages
                    for page in pages:
                        text = page.extract_text()
                        if text:
                            full_text += text + ' \n '
            return full_text

        except Exception as e:
            return str(e)
 
