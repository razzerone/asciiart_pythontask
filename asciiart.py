import argparse
import sys
from pathlib import Path

from PIL import Image

from ASCIIArtCore.art_processor import ArtProcessor
from ASCIIArtCore.image_printer import ImagePrinter
from ASCIIArtCore.text_printer import TextPrinter


def asciiart(path: Path):
    try:
        img = Image.open(path)
    except IOError:
        print(f'Не удалось найти изображение по заданному пути {path}')
        sys.exit(1)

    art = ArtProcessor.process_image_to_asciiart(img)

    image_printer = ImagePrinter(img.width, img.height)
    text_printer = TextPrinter()

    for char, color in art:
        image_printer.add_char(char, color)
        text_printer.add_char(char)
            
    image_printer.save(Path.cwd() / f'asciiart_{path.stem}.png')
    text_printer.save(Path.cwd() / f'asciiart_{path.stem}.txt')


def main():
    parser = argparse.ArgumentParser(
        description='Переводит изображение в ASCII арт'
    )
    parser.add_argument('image', help='Путь к изображению')
    args = parser.parse_args()

    asciiart(Path(args.image))


if __name__ == '__main__':
    main()
