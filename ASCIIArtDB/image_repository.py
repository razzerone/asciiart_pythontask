from threading import Timer

from sqlalchemy.orm import sessionmaker

from ASCIIArtDB.SQL_impl import engine, Image
from ASCIIArtDB.repository import Repository


class ImageRepository(Repository):
    def __init__(self, engine=None):
        self._engine = engine
        self._session_factory = sessionmaker(bind=engine)

        self._delete_timer = Timer(60 * 30, self._delete_old_images)
        self._delete_timer.start()

    def add_image(self, img_bin: bytes) -> int:
        session = self._session_factory()
        image = Image(
            image=img_bin,
            timestamp=Repository.get_current_timestamp()
        )
        session.add(image)
        session.commit()
        return image.id

    def get_image_by_id(self, id_) -> bytes:
        session = self._session_factory()
        resp = session.query(Image.image).filter(Image.id == id_).one()
        session.commit()
        return resp

    def _delete_old_images(self):
        session = self._session_factory()
        session.query(Image) \
            .filter(
            Repository.get_current_timestamp() - Image.timestamp >= 3000
        ) \
            .delete()

        session.commit()
