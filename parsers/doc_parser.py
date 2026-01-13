from docx import Document


class documnetParser:
    def __init__(self, filename):
        self.filename = filename

    def extract_all_text(self):
        all_text = ''
        try:
            file = Document(self.filename)
            
            for doc in file.paragraphs:
                if doc.text:
                    all_text += doc.text + " \n "
            return all_text
        except:
            return "no text extracted"

