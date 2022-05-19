import io
import secrets

import flask
from PIL import Image

from ASCIIArtCore.art_processor import ArtProcessor
from ASCIIArtCore.image_printer import ImagePrinter
from ASCIIArtCore.text_printer import TextPrinter


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_bytes()


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


def uploading(func, fmt):
    if flask.request.method == 'POST':
        if 'photo' not in flask.request.files:
            flask.flash('No file part')
            return flask.redirect(flask.request.url)

        image = flask.request.files['photo']

        if image.filename == '':
            flask.flash('No selected file')
            return flask.redirect(flask.request.url)

        return func(image.stream.read())

    elif flask.request.method == 'GET':
        return flask.render_template(
            'upload.html',
            action=flask.url_for(f'asciiart_{fmt}'),
            format=fmt
        )


@app.route('/', methods=('GET', ))
def index():
    return flask.render_template(
        'index.html',
        image_url=flask.url_for('asciiart_image'),
        text_url=flask.url_for('asciiart_text')
    )


@app.route('/upload_image', methods=('POST', 'GET'))
def asciiart_image():
    return uploading(get_asciiart_image, 'image')


@app.route('/upload_text', methods=('POST', 'GET'))
def asciiart_text():
    return uploading(get_asciiart_text, 'text')


if __name__ == '__main__':
    app.run()
