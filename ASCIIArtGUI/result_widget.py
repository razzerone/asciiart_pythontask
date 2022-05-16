from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSplashScreen, \
    QFileDialog, QHBoxLayout, QCheckBox
from PyQt6 import QtGui

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

        self.check_box = None

        self.text_widget = None
        self.splash = None

        self.setup()

    def setup(self):
        layout = QGridLayout(self)

        show_text_btn = QPushButton('Текст')
        show_text_btn.clicked.connect(self.show_text)
        layout.addWidget(show_text_btn, 0, 0)

        show_image_btn = QPushButton('Изображение')
        show_image_btn.clicked.connect(self.show_image)
        layout.addWidget(show_image_btn, 1, 0)

        self.check_box = QCheckBox("в приложении по умолчанию")
        layout.addWidget(self.check_box, 1, 1)

        save_text_btn = QPushButton('Сохранить текст')
        save_text_btn.clicked.connect(self.save_text)
        layout.addWidget(save_text_btn, 2, 0)

        save_image_btn = QPushButton('Сохранить изображение')
        save_image_btn.clicked.connect(self.save_image)
        layout.addWidget(save_image_btn, 3, 0)
        self.splash = QSplashScreen(QtGui.QPixmap('fresco.png'))

    def _process_image(self):
        if self.image is None:
            self.image = ImagePrinter(self.art).get_image()
            self.splash.show()
            QTimer.singleShot(2000, self.splash.close)

    def _process_text(self):
        if self.text is None:
            self.text = TextPrinter(self.art).get_text()
            self.splash.show()
            QTimer.singleShot(2000, self.splash.close)

    def show_image(self):
        self._process_image()

        if self.check_box.isChecked():
            self.image.show()

    def show_text(self):
        self._process_text()
        self.text_widget = TextWidget(self.text)
        self.text_widget.showMaximized()

    def save_image(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Выбор файла",
            "",
            "Image Files (*.png),*.png",
        )
        self.image.save(path)

    def save_text(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Выбор файла",
            "",
            "Text Files (*.txt),*.txt",
        )
        with open(path, 'w') as f:
            f.write(self.text)
