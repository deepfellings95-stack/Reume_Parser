import PyPDF2
from PyPDF2 import PdfReader

class pdfParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.reader = None

    def extract_all_text(self):
        full_text = ''
        try:
            with open(self.filepath, 'rb') as f:
                self.reader = PdfReader(f)
                pages = self.reader.pages
                for page in pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + ' \n '
            return full_text
        except Exception as e:
            print(f'exception occure {e}')
            print(f'error {e}')
 
