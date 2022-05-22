import io
import secrets

import flask
from PIL import Image

from ASCIIArtCore.art_processor import ArtProcessor
from ASCIIArtCore.image_printer import ImagePrinter
from ASCIIArtCore.text_printer import TextPrinter
from ASCIIArtDB.image_repository_SQL import ImageRepositoryImpl
from ASCIIArtDB.tables import engine

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_bytes()

image_repo = ImageRepositoryImpl(engine=engine)


def get_asciiart_text(img_bytes: bytes):
    img = Image.open(io.BytesIO(img_bytes))
    art = ArtProcessor.process_image_to_asciiart(img)
    text_printer = TextPrinter()

    for char, color in art:
        text_printer.add_char(char)

    return flask.render_template(
        'text_output.html',
        text=text_printer.get_text()
    )


def get_asciiart_image(img_bytes: bytes):
    img = Image.open(io.BytesIO(img_bytes))
    art = ArtProcessor.process_image_to_asciiart(img)
    image_printer = ImagePrinter(img.width, img.height)

    for char, color in art:
        image_printer.add_char(char, color)

    return serve_pil_image(image_printer.get_image())


def serve_pil_image(pil_image: Image.Image):
    img_io = io.BytesIO()
    pil_image.save(img_io, "png")
    img_io.seek(0)
    return flask.send_file(img_io, mimetype='image/png')


def get_result(func):
    try:
        id_ = flask.session['image_id']
    except:
        return \
            'Извините, но ваше изображение потерялось (возможно его и не было)'

    img_bin = image_repo.get_image_by_id(id_)

    if img_bin is None:
        return \
            'Извините, но ваше изображение потерялось (возможно его и не было)'

    image_repo.delete_old_images()

    return func(img_bin)


@app.route('/', methods=('GET', ))
def index():
    return flask.render_template(
        'index.html',
        action=flask.url_for('upload')
    )


@app.route('/upload', methods=('GET', 'POST'))
def upload():
    if flask.request.method == 'POST':
        if 'photo' not in flask.request.files:
            flask.flash('No file part')
            return flask.redirect(flask.request.url)

        image = flask.request.files['photo']

        if image.filename == '':
            flask.flash('No selected file')
            return flask.redirect(flask.request.url)

        id_ = image_repo.add_image(image.stream.read())

        flask.session['image_id'] = id_

        return flask.redirect(flask.url_for('result'))

    return flask.redirect(flask.url_for('/'))


@app.route('/result', methods=('GET', ))
def result():
    return flask.render_template(
        'result_main.html',
        text_url=flask.url_for('result_text'),
        image_url=flask.url_for('result_image')
    )


@app.route('/result/text', methods=('GET', ))
def result_text():
    return get_result(get_asciiart_text)


@app.route('/result/image', methods=('GET', ))
def result_image():
    return get_result(get_asciiart_image)


if __name__ == '__main__':
    app.run()
