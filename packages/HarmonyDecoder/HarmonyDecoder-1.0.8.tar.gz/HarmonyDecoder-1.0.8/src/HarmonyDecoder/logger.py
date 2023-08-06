from PyQt5.QtWidgets import QTextEdit
from datetime import datetime

class logger:
    def __init__(self, box:QTextEdit):
        self.box:QTextEdit = box

    def log(self, what:str) -> None:
        self.box.append(f"{datetime.now().time()}: {what}")