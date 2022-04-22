import os
from pathlib import Path
from unittest import TestCase

from PIL import Image

import settings
from ASCIIArtCore.art_processor import ArtProcessor
from ASCIIArtCore.image_printer import ImagePrinter
from ASCIIArtCore.text_printer import TextPrinter
from asciiart import asciiart


class ArtProcessorTest(TestCase):
    def setUp(self):
        self.img = Image.open('assets/a.jpg')
        self.art = list(ArtProcessor.process_image_to_asciiart(self.img))

    def test_make_asciiart_correct(self):
        self.assertEquals(
            '\n',
            self.art[self.img.width]
        )

    def test_process_pixel_lowest_brightness(self):
        self.assertEquals(
            ArtProcessor.process_pixel_to_char((0, 0, 0)),
            settings.ASCII_symbols[0]
        )

    def test_process_pixel_highest_brightness(self):
        self.assertEquals(
            ArtProcessor.process_pixel_to_char((255, 255, 255)),
            settings.ASCII_symbols[-1]
        )


class TextPrinterTest(TestCase):
    def setUp(self):
        self.path_txt = Path('abc.txt')
        self.tp = TextPrinter()

    def tearDown(self) -> None:
        os.remove(self.path_txt)

    def test_print_art_in_text_file_correct(self):
        self.tp.add_char('q')
        self.tp.save(self.path_txt)
        self.assertTrue(self.path_txt.exists())

    def test_print_art_in_text_file_with_existing_file(self):
        with self.path_txt.open('x') as f:
            pass

        with self.assertRaises(SystemExit):
            self.tp.add_char('q')
            self.tp.save(self.path_txt)

    def test_print_empty_art(self):
        with self.assertRaises(Exception):
            self.tp.save(self.path_txt)


class ImagePrinterTest(TestCase):
    def setUp(self) -> None:
        self.img = Image.open('assets/a.jpg')
        self.path_img = Path('abc.png')
        self.ip = ImagePrinter(1, 1)

    def tearDown(self) -> None:
        os.remove(self.path_img)

    def test_print_art_in_image_file_correct(self):
        self.ip.add_char('q')
        self.ip.save(self.path_img)
        self.assertTrue(self.path_img.exists())

    def test_print_art_in_image_file_with_existing_file(self):
        with self.path_img.open('x'):
            pass

        with self.assertRaises(SystemExit):
            self.ip.add_char('q')
            self.ip.save(self.path_img)

    def test_print_empty_art(self):
        with self.assertRaises(Exception):
            self.ip.get_image()


class CommonTest(TestCase):
    def setUp(self) -> None:
        self.path = Path('assets/a.jpg')
        self.dest_txt_path = Path.cwd() / f'asciiart_{self.path.stem}.txt'
        self.dest_png_path = Path.cwd() / f'asciiart_{self.path.stem}.png'

    def tearDown(self) -> None:
        if self.dest_txt_path.exists():
            os.remove(self.dest_txt_path)
        if self.dest_png_path.exists():
            os.remove(self.dest_png_path)

    def test_asciiart_correct(self):
        asciiart(self.path)
        self.assertTrue(self.dest_png_path.exists())
        self.assertTrue(self.dest_txt_path.exists())

    def test_asciiart_img_not_exist(self):
        with self.assertRaises(SystemExit):
            asciiart(Path('1234321'))
