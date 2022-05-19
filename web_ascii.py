import io
import secrets
import tempfile

import flask
from PIL import Image

from ASCIIArtCore.art_processor import ArtProcessor
from ASCIIArtCore.image_printer import ImagePrinter
from ASCIIArtCore.text_printer import TextPrinter


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_bytes()

pull = dict()


def get_asciiart(image: bytes):
    img = Image.open(io.BytesIO(image))

    art = ArtProcessor.process_image_to_asciiart(img)

    image_printer = ImagePrinter(img.width, img.height)
    text_printer = TextPrinter()

    for char, color in art:
        image_printer.add_char(char, color)
        text_printer.add_char(char)

    return text_printer.get_text(), image_printer.get_image()


def serve_pil_image(pil_image: Image.Image):
    img_io = io.BytesIO()
    pil_image.save(img_io, "png")
    img_io.seek(0)
    return flask.send_file(img_io, mimetype='image/png')


@app.route('/show/')
def show(path):
    pass


@app.route('/', methods=('GET', ))
def index():
    return flask.render_template('index.html')


@app.route('/upload', methods=('POST', 'GET'))
def asciiart():
    if flask.request.method == 'POST':
        if 'photo' not in flask.request.files:
            flask.flash('No file part')
            return flask.redirect(flask.request.url)

        image = flask.request.files['photo']

        if image.filename == '':
            flask.flash('No selected file')
            return flask.redirect(flask.request.url)

        _, img = get_asciiart(image.stream.read())

        return serve_pil_image(img)

    elif flask.request.method == 'GET':
        return flask.render_template('image.html', image_path=pull[flask.request.remote_addr])
# C:\Users\RAZZER~1\AppData\Local\Temp\tmpt8wszidb

if __name__ == '__main__':
    app.run()
