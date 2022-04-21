import argparse
import sys
from collections.abc import Iterable
from pathlib import Path

import cv2
import numpy

import settings

from PIL import Image, ImageFont, ImageDraw


class ASCIIArt:
    """
    Функция получает на вход изображение и возвращает готовый ascii арт в виде
    итератора с разделениями на строки
    """

    @staticmethod
    def process_image_to_asciiart(img: Image.Image) -> Iterable[str]:
        count = 0
        for p in img.getdata():
            yield settings.ASCII_symbols[
                (p[0] + p[1] + p[2]) / 3 // settings.contrast_step]
            count += 1
            if count == img.width:
                yield '\n'
                count = 0

    @staticmethod
    def process_pixel_to_char(pixel):
        return (pixel[0] + pixel[1] + pixel[2]) / 3 // settings.contrast_step


class ImagePrinter:
    def __init__(self, width, height):
        self.img = numpy.asarray(Image.new('RGB', (width * 12, height * 17)))
        self.x = 0
        self.y = 0

    def print_char(self, char):
        if char == '\n':
            self.y += 1
            self.x = 0
        else:
            # печатает по одному пикселю (букве)
            cv2.putText(
                self.img, char,
                (
                    self.x * settings.image_font_width,
                    self.y * settings.image_font_height
                ),
                settings.image_font,
                settings.image_font_size,
                (150, 150, 150),
                thickness=1, lineType=cv2.LINE_4
            )

            self.x += 1

    def save_image(self, path):
        Image.fromarray(self.img).save(path)


class Output:
    """
    Функция печатает ascii арт в текстовый файл по указанному пути

    Если файл с таким именем уже существует, будет выведено сообщение
    и приложение завершит работу
    """

    @staticmethod
    def print_art_in_text_file(path: Path, art: str) -> None:
        if path.exists():
            print(f'Текстовый файл с именем {path.name} уже существует')
            sys.exit(1)

        with path.open('w') as file:
            file.write(art)

    """
    Функция сохраняет изображение с ascii артом в файл в формате png 
    по заданному пути
    
    Если файл с таким именем уже существует, будет выведено сообщение
    и приложение завершит работу
    """

    @staticmethod
    def print_art_in_image_file(path: Path, art: Image.Image) -> None:
        if path.exists():
            print(f'Файл изображения с именем {path.name} уже существует')
            sys.exit(1)

        art.save(path)


def asciiart(path: Path) -> None:
    try:
        img = Image.open(path)
    except IOError:
        print(f'Не удалось найти изображение по заданному пути {path}')
        sys.exit(1)

    art = ASCIIArt.process_image_to_asciiart(img)

    ip = ImagePrinter(img.width, img.height)

    with open(Path.cwd() / f'asciiart_{path.stem}.txt') as f:
        for c in art:
            # в цикле печатает на изображение и в файл
            ip.print_char(c)
            f.write(c)

    ip.save_image(Path.cwd() / f'asciiart_{path.stem}.png')


def main():
    parser = argparse.ArgumentParser(
        description='Переводит изображение в ASCII арт'
    )
    parser.add_argument('image', help='Путь к изображению')
    args = parser.parse_args()

    asciiart(Path(args.image))


if __name__ == '__main__':
    main()
