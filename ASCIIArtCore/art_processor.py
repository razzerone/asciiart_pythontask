from typing import Iterable, Tuple

from PIL.Image import Image

import settings


class ArtProcessor:

    @staticmethod
    def process_image_to_asciiart(img: Image) -> Iterable[str]:
        """
            Функция получает на вход изображение и возвращает готовый ascii арт
            в виде итератора с разделениями на строки
        """

        count = 0
        for p in img.getdata():
            yield ArtProcessor.process_pixel_to_char(p)
            count += 1
            if count == img.width:
                yield '\n'
                count = 0

    @staticmethod
    def process_pixel_to_char(pixel: Tuple) -> str:
        """
            Ставится однозначное соответствие пикселю в виде символа ASCII.
        """

        return settings.ASCII_symbols[
            (pixel[0] + pixel[1] + pixel[2]) / 3 // settings.contrast_step
            ]
