from docx import Document
import zipfile
import os
from parsers.image_parser2 import imageParser


class documentParser:
    def __init__(self, filename):
        self.filename = filename

    def extract_all_text(self):
        all_text = ''
        filepath = self.filename
        
        try:
            file = Document(filepath)
                
            for doc in file.paragraphs:
                if doc.text:
                    all_text += doc.text.strip() + " \n "
                    
                    
            with zipfile.ZipFile(filepath, 'r') as docx:
                for file in docx.namelist():
                    if file.startswith('word/media/'):
                        img_data = docx.read(file)
                        img_filename = file.split("/")[-1]
                        out_path = os.path.join("upload/", f"img_{img_filename}")

                        
                        with open(out_path, "wb") as f:
                            f.write(img_data)
                        
                        text = imageParser(out_path).extract_all_text()
                        if text:
                            all_text += text.strip() + "\n"

            
            
            if not all_text.strip(): 
                all_text = "something went wrong during parsing"
            return all_text
        except Exception as e:
            return e

