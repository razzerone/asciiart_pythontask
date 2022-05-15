import os
import sys

from PIL import Image
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox, QFileDialog, \
    QLabel

from ASCIIArtCore.art_processor import ArtProcessor
from ASCIIArtGUI.result_widget import ResultWidget


class StartWidget(QWidget):
    file_name: os.PathLike

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):

        asciiart_btn = QPushButton('Сделать asciiart', self)

        asciiart_btn.resize(100, 32)
        asciiart_btn.move(50, 50)
        asciiart_btn.clicked.connect(self.asciiart)

        asciiart_btn.hide()

        file_btn = QPushButton('Выберите файл', self)


        file_btn.resize(100, 32)
        file_btn.move(50, 100)

        file_btn.clicked.connect(lambda: self.openFileNameDialog(asciiart_btn))

        text = QLabel('at the beginning', self)
        text.setFont(QFont('Courier', 4))

    def openFileNameDialog(self, btn):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выбор файла",
            "",
            "Image Files (*.jpeg;*.jpg;*.png),*.jpeg;*.jpg;*.png",
        )
        self.file_name = file_name

        btn.show()

    def asciiart(self) -> None:
        try:
            img = Image.open(self.file_name)
        except IOError:
            print(f'Не удалось найти изображение по заданному пути {self.file_name}')
            sys.exit(1)
        art = ArtProcessor.get_ascii_art(img)
        self.parent().setCentralWidget(ResultWidget(art))
