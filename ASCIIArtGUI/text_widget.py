from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea


class TextWidget(QWidget):
    def __init__(self, text: str):
        super().__init__()
        self.text = text


        self.scroll = QScrollArea(self)
        self.scroll.resize(1920, 1080)

        label = QLabel(self.text)
        label.setFont(QFont('Courier', 2))

        self.scroll.setWidget(label)

        self.show()



