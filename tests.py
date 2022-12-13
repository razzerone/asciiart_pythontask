import datetime
import io
import os
import unittest
from pathlib import Path
from unittest import TestCase

import flask
from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import ASCIIArtDB.tables
import settings
import web_ascii
from ASCIIArtCore.art_processor import ArtProcessor
from ASCIIArtCore.image_printer import ImagePrinter
from ASCIIArtCore.text_printer import TextPrinter
from ASCIIArtDB.image_repository_SQL import ImageRepositoryImpl
from asciiart import asciiart
from domain.names import IMAGE_ID
from web_ascii import app


class ArtProcessorTest(TestCase):
    def setUp(self):
        self.img = Image.open('assets/a.jpg')
        self.art = list(ArtProcessor.process_image_to_asciiart(self.img))

    def test_make_asciiart_correct(self):
        self.assertEqual(
            '\n',
            self.art[self.img.width][0]
        )

    def test_process_pixel_lowest_brightness(self):
        self.assertEqual(
            ArtProcessor.process_pixel_to_char((0, 0, 0)),
            settings.ASCII_symbols[0]
        )

    def test_process_pixel_highest_brightness(self):
        self.assertEqual(
            ArtProcessor.process_pixel_to_char((255, 255, 255)),
            settings.ASCII_symbols[256 // settings.contrast_step]
        )


class TextPrinterTest(TestCase):
    def setUp(self):
        self.path_txt = Path('abc.txt')
        self.tp = TextPrinter()

    def tearDown(self) -> None:
        if self.path_txt.exists():
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
        self.img.close()
        if self.path_img.exists():
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


class ViewTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app
        app.config['SECRET_KEY'] = 'sekrit!'
        self.engine = create_engine('sqlite:///test.db', echo=True)
        ASCIIArtDB.tables.Base.metadata.create_all(self.engine)
        self.repo = ImageRepositoryImpl(self.engine)
        web_ascii.image_repo = self.repo

        with open('assets/a.jpg', 'rb') as f:
            self.repo.add_image(f.read())

    def tearDown(self) -> None:
        sm = sessionmaker(self.engine)
        with sm() as s:
            s.query(ASCIIArtDB.tables.Image).delete()
            s.commit()

    def test_index_ok(self):
        response = self.app.test_client().get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/html')
        self.assertGreater(len(response.data), 0)

    def test_upload_get_redirect(self):
        response = self.app.test_client().get('/upload')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.mimetype, 'text/html')
        self.assertGreater(len(response.data), 0)

    def test_upload_post_empty_request_redirect(self):
        with self.app.test_client() as cl:
            response = cl.post('/upload', data={})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.mimetype, 'text/html')
            self.assertGreater(len(response.data), 0)

    def test_upload_post_empty_filename_redirect(self):
        with self.app.test_client() as cl:
            response = cl.post(
                '/upload',
                data={'photo': (io.BytesIO(), '')}
            )
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.mimetype, 'text/html')
            self.assertGreater(len(response.data), 0)

    def test_upload_post_file_redirect(self):
        with self.app.test_client() as cl:
            response = cl.post(
                '/upload',
                data={'photo': (io.BytesIO(b'123123123'), 'pic')}
            )
            self.assertIsNotNone(flask.session[IMAGE_ID])
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.mimetype, 'text/html')
            self.assertGreater(len(response.data), 0)

    def test_result_get_ok(self):
        response = self.app.test_client().get('/result')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/html')
        self.assertGreater(len(response.data), 0)

    def test_result_text_get_unexisting_image_404(self):
        response = self.app.test_client().get('/result/text')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, 'text/html')
        self.assertGreater(len(response.data), 0)

    def test_result_image_get_unexisted_image_404(self):
        response = self.app.test_client().get('/result/image')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, 'text/html')
        self.assertGreater(len(response.data), 0)

    def test_result_text_get_invalid_image_404(self):
        with self.app.test_client() as cl:
            with cl.session_transaction() as session:
                session[IMAGE_ID] = 9999999

            response = cl.get('/result/text')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.mimetype, 'text/html')
            self.assertGreater(len(response.data), 0)

    def test_result_image_get_invalid_image_404(self):
        with self.app.test_client() as cl:
            with cl.session_transaction() as session:
                session[IMAGE_ID] = 9999999

            response = cl.get('/result/image')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.mimetype, 'text/html')
            self.assertGreater(len(response.data), 0)

    def test_result_text_get_image_ok(self):
        with self.app.test_client() as cl:
            with cl.session_transaction() as session:
                session[IMAGE_ID] = 1

            response = cl.get('/result/text')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, 'text/html')
            self.assertGreater(len(response.data), 0)

    def test_result_image_get_image_ok(self):
        with self.app.test_client() as cl:
            with cl.session_transaction() as session:
                session[IMAGE_ID] = 1

            response = cl.get('/result/image')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, 'image/png')
            self.assertGreater(len(response.data), 0)


class ImageRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine('sqlite:///test.db', echo=True)
        ASCIIArtDB.tables.Base.metadata.create_all(self.engine)
        self.sm = sessionmaker(self.engine)

        self.repo = ImageRepositoryImpl(self.engine)
        web_ascii.image_repo = self.repo

    def tearDown(self) -> None:
        with self.sm() as s:
            s.query(ASCIIArtDB.tables.Image).delete()
            s.commit()

    def test_add_image_correct(self):
        self.repo.add_image(b'12312344321')

        with self.sm() as s:
            imgs = s.query(ASCIIArtDB.tables.Image).all()
            s.commit()

            self.assertEqual(len(imgs), 1)

    def test_add_image_not_rewrite_image(self):
        self.repo.add_image(b'12312344321')
        self.repo.add_image(b'12312344321')

        with self.sm() as s:
            imgs = s.query(ASCIIArtDB.tables.Image).all()
            s.commit()

            self.assertEqual(len(imgs), 2)
            self.assertEqual(imgs[0].image, imgs[1].image)
            self.assertNotEqual(imgs[0].id, imgs[1].id)

    def test_get_image_by_id_correct(self):
        img_s = b'12312344321'
        id_ = self.repo.add_image(img_s)
        img = self.repo.get_image_by_id(id_)

        self.assertEqual(img_s, img)

    def test_get_image_by_id_unexisting_image(self):
        img = self.repo.get_image_by_id(1)

        self.assertIsNone(img)

    def test_delete_old_images_correct(self):
        with self.sm() as s:
            s.add(ASCIIArtDB.tables.Image(
                image=b'123', timestamp=19990101010101
            ))
            s.commit()

        self.repo.delete_old_images()

        with self.sm() as s:
            count = s.query(ASCIIArtDB.tables.Image).count()

            self.assertEqual(count, 0)

    def test_delete_old_images_not_delete_new_images(self):
        with self.sm() as s:
            s.add(ASCIIArtDB.tables.Image(
                image=b'123', timestamp=20230101010101
            ))
            s.commit()

        self.repo.delete_old_images()

        with self.sm() as s:
            count = s.query(ASCIIArtDB.tables.Image).count()

            self.assertEqual(count, 1)

    def test_get_current_timestamp(self):
        ts = str(ImageRepositoryImpl.get_current_timestamp())

        self.assertEqual(14, len(ts))
        self.assertEqual(str(datetime.datetime.now().year), ts[0:4])



