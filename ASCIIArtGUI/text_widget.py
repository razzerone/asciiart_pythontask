from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QScrollArea, QMainWindow


class TextWidget(QWidget):
    def __init__(self, text: str):
        super().__init__()
        self.text = text

        self.scroll = None

        self.setup()

    def setup(self):
        self.scroll = QScrollArea(self)
        self.scroll.resize(1920, 1080)

        label = QLabel(self.text)
        label.setFont(QFont('Courier', 8))

        self.scroll.setWidget(label)

