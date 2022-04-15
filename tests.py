import os
from pathlib import Path
from unittest import TestCase

from PIL import Image

import settings
from asciiart import ASCIIArt, Output, asciiart


class ASCIIArtTest(TestCase):
    def setUp(self):
        self.img = Image.open('a.jpg')
        self.art = list(ASCIIArt.make_asciiart(self.img))

    def test_make_asciiart_correct(self):
        self.assertEquals(
            '\n',
            self.art[self.img.width]
        )

    def test_process_art_to_image_correct(self):
        img_art = ASCIIArt.process_art_to_image(
            ''.join(self.art), self.img.width, self.img.height
        )
        self.assertNotEquals(self.img.width, img_art.width)
        self.assertNotEquals(self.img.height, img_art.height)


class OutputTxtTest(TestCase):
    def setUp(self):
        self.path_txt = Path('abc.txt')

    def tearDown(self) -> None:
        os.remove(self.path_txt)

    def test_print_art_in_text_file_correct(self):
        Output.print_art_in_text_file(self.path_txt, 'abc')
        self.assertTrue(self.path_txt.exists())

    def test_print_art_in_text_file_with_existing_file(self):
        with self.path_txt.open('x') as f:
            pass

        with self.assertRaises(SystemExit):
            Output.print_art_in_text_file(self.path_txt, 'abc')


class OutputImgTest(TestCase):
    def setUp(self) -> None:
        self.img = Image.open('a.jpg')
        self.path_img = Path('abc.png')

    def tearDown(self) -> None:
        os.remove(self.path_img)

    def test_print_art_in_image_file_correct(self):
        Output.print_art_in_image_file(self.path_img, self.img)
        self.assertTrue(self.path_img.exists())

    def test_print_art_in_image_file_with_existing_file(self):
        with self.path_img.open('x') as f:
            pass

        with self.assertRaises(SystemExit):
            Output.print_art_in_image_file(self.path_img, self.img)


class CommonTest(TestCase):
    def setUp(self) -> None:
        self.path = Path('a.jpg')
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
