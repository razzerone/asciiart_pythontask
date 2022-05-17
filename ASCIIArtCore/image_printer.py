import sys
from pathlib import Path
from threading import Thread

import cv2
import numpy
from PIL import Image

import settings
from ASCIIArtCore.art_processor import Art


class ImagePrinter:
    _is_ready: bool

    def __init__(self, width, height):
        self._is_ready = False
        self._thread = None

        self.img = numpy.full(
            (
                height * settings.image_font_height,
                width * settings.image_font_width,
                3
            ),
            45,
            dtype=numpy.uint8
        )

        self.x = 0
        self.y = 0

    def __init__(self, art: Art):
        self._is_ready = False
        self._thread = None

        self.img = numpy.full(
            (
                art.height * settings.image_font_height,
                art.width * settings.image_font_width,
                3
            ),
            45,
            dtype=numpy.uint8
        )

        self.x = 0
        self.y = 0

        for char, color in art.art:
            self.add_char(char, color)

    def add_all_chars(self, art):
        for char, color in art.art:
            self.add_char(char, color)

        self._is_ready = True

    def from_art_paralel(self, art: Art):
        self._thread = Thread(target=self.add_all_chars, args=(art, ))
        self._thread.start()


    def add_char(self, char: str,
                 color: tuple[int, int, int] = (255, 255, 255)) -> None:
        if char == '\n':
            self.y += 1
            self.x = 0
        else:
            cv2.putText(
                self.img, char,
                (
                    self.x * settings.image_font_width,
                    self.y * settings.image_font_height
                ),
                settings.image_font,
                settings.image_font_size,
                color,
                thickness=settings.image_font_thickness,
                lineType=settings.image_font_line_type
            )

            self.x += 1

    def get_image(self) -> Image.Image:
        if self.x == 0 and self.y == 0:
            raise Exception(
                'Арт для печати на изображение не может быть пустым'
            )

        return Image.fromarray(self.img)

    def save(self, path: Path) -> None:
        """ 
            Функция сохраняет изображение с ascii артом в файл в формате png
            по заданному пути
            Если файл с таким именем уже существует, будет выведено сообщение
            и приложение завершит работу
        """

        if path.exists():
            print(f'Файл изображения с именем {path.name} уже существует')
            sys.exit(1)

        self.get_image().save(path)
