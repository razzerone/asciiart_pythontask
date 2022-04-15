import argparse
import sys
from collections.abc import Iterable
from pathlib import Path

import settings

from PIL import Image, ImageFont, ImageDraw


class ASCIIArt:
    """
    Функция получает на вход изображение и возвращает готовый ascii арт в виде
    итератора с разделениями на строки
    """
    @staticmethod
    def make_asciiart(img: Image.Image) -> Iterable[str]:
        return ASCIIArt._convert_to_ascii(img.convert('L'))

    """
    Функция принимает строку и размеры ascii арта и возвращает изображение, на
    котором арт напечатан 
    
    Для работы этой функции необходим файл с моноширинным шрифтом
    """
    @staticmethod
    def process_art_to_image(art: str, width: int, height: int) -> Image.Image:

        # получить размер шрифта в пикселях мы так и не смогли
        image = Image.new('RGB', (width * 9, height * 11))
        image_font = ImageFont.truetype(
            settings.image_font,
            settings.image_font_size
        )
        im_draw = ImageDraw.Draw(image)
        im_draw.text((0, 0), art, font=image_font)

        return image

    @staticmethod
    def _convert_to_ascii(img: Image.Image) -> Iterable[str]:
        count = 0
        for p in img.getdata():
            yield settings.ASCII_symbols[p // settings.contrast_step]
            count += 1
            if count == img.width:
                yield '\n'
                count = 0


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

    art = ''.join(ASCIIArt.make_asciiart(img))

    Output.print_art_in_text_file(
        Path.cwd() / f'asciiart_{path.stem}.txt',
        art
    )

    Output.print_art_in_image_file(
        Path.cwd() / f'asciiart_{path.stem}.png',
        ASCIIArt.process_art_to_image(art, img.width, img.height)
    )


def main():
    parser = argparse.ArgumentParser(
        description='Переводит изображение в ASCII арт'
    )
    parser.add_argument('image', help='Путь к изображению')
    args = parser.parse_args()

    asciiart(Path(args.image))


if __name__ == '__main__':
    main()
