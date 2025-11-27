class textParser:
    def __init__(self, filename):
        self.filename = filename

    def extract_all_text(self):

        full_text = ''
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    full_text += line.strip() + ' \n '

            return full_text
        except Exception as e:
            return f"error {e}"
        
