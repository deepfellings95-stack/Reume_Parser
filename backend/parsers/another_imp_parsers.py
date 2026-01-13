import subprocess
import pypandoc
from docx import Document
from odf.opendocument import load
from odf.text import P
import os
import tempfile
from parsers.doc_parser import documentParser
from parsers.image_parser2 import imageParser
from parsers.pypdf2_parser import pdfParser
import aspose.words as aw
from flask import current_app


class UniversalDocParser:
    def __init__(self, filepath):
        self.filepath = filepath
        
    def extract_doc(self):
        try:
            temp_doc = tempfile.mktemp(suffix=".docx")
            pypandoc.convert_file(self.filepath, "docx", outputfile=temp_doc)
            all_text = documentParser(temp_doc)
            all_text = all_text.extract_all_text()
            
            return all_text
        except Exception as e:
            return str(e)
            
    def extract_rtf(self):
        try:
            temp_docx = tempfile.mktemp(suffix=".docx")
            pypandoc.convert_file(self.filepath, "docx", outputfile=temp_docx)
            all_text = documentParser(temp_docx)
            all_text = all_text.extract_all_text()
                
            return all_text
        except Exception as e:
            return str(e)
            
            
    def extract_odt(self):
        try:
            text = load(self.filepath)
            para =  text.getElementsByType(P)
            all_text = "\n".join(
                ["".join(node.data for node in p.childNodes if hasattr(node, "data")) for p in para]
            ).strip()
            
            if not all_text:
                folder, filename = os.path.split(self.filepath)
                name, _ = os.path.splitext(filename)
                folder = current_app.config['CONVERT_FOLDER']
                path = os.path.join(folder, f"{name}.pdf")
                
                pypandoc.convert_file(self.filepath, "docx", outputfile=path)
              
                
                all_text = documentParser(path)
                all_text = all_text.extract_all_text()
            
            return all_text
        except Exception as e:
            return str(e)
            
    def extract_all_text(self):
        ext = self.filepath.rsplit('.',1)[1].lower()
        
        if ext == 'doc':
            return self.extract_doc()
            
        elif ext == 'rtf':
            return self.extract_rtf()
            
        elif ext == 'odt':
            return self.extract_odt()
        else:
            return "nothing"
        