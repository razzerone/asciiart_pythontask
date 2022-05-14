from PIL import Image
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton

from ASCIIArtCore.art_processor import Art
from ASCIIArtCore.image_printer import ImagePrinter
from ASCIIArtCore.text_printer import TextPrinter
from ASCIIArtGUI.text_widget import TextWidget


class ResultWidget(QWidget):
    def __init__(self, art: Art):
        super().__init__()

        self.art = art
        self.text = None
        self.image = None

        self.label = None

        layout = QGridLayout(self)

        show_text_btn = QPushButton('Текст')
        show_text_btn.clicked.connect(self.show_text)
        layout.addWidget(show_text_btn)

        show_image_btn = QPushButton('Изображение')
        show_image_btn.clicked.connect(self.show_text)
        layout.addWidget(show_image_btn)

        save_text_btn = QPushButton('Сохранить текст')
        save_text_btn.clicked.connect(self.show_text)
        layout.addWidget(save_text_btn)

        save_image_btn = QPushButton('Сохранить изображение')
        save_image_btn.clicked.connect(self.show_text)
        layout.addWidget(save_image_btn)

    def _process_image(self):
        if self.image is None:
            self.image = ImagePrinter(self.art).get_image()

    def _process_text(self):
        if self.text is None:
            self.text = TextPrinter(self.art).get_text()

    def show_image(self):
        self._process_image()
        self.image.show()

    def show_text(self):
        self._process_text()
        self.label = TextWidget(self.text)

    def save_image(self):
        pass

    def save_text(self):
        pass