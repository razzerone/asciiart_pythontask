import sys
from pathlib import Path

import cv2
import numpy
from PIL import Image

import settings


class ImagePrinter:

    def __init__(self, width, height):
        self.img = numpy.asarray(
            Image.new(
                'RGB',
                (
                    width * settings.image_font_width,
                    height * settings.image_font_height
                )
            )
        )
        self.x = 0
        self.y = 0

    def add_char(self, char: str) -> None:
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
                (120, 120, 120),
                thickness=settings.image_font_thickness,
                lineType=settings.image_font_line_type
            )

            self.x += 1

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

        Image.fromarray(self.img).save(path)
