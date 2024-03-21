class ExistORMObject(Exception):
    def __init__(self, text: str):
        self.text = text
