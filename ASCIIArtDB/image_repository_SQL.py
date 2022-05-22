from sqlalchemy.orm import sessionmaker

from ASCIIArtDB.tables import Image
from ASCIIArtDB.image_repository import ImageRepository


class ImageRepositoryImpl(ImageRepository):
    def __init__(self, engine=None):
        self._engine = engine
        self._session_factory = sessionmaker(bind=engine)

    def add_image(self, img_bin: bytes) -> int:
        session = self._session_factory()
        image = Image(
            image=img_bin,
            timestamp=ImageRepositoryImpl.get_current_timestamp()
        )
        session.add(image)
        session.commit()
        return image.id

    def get_image_by_id(self, id_: int) -> bytes:
        session = self._session_factory()
        resp = session.query(Image.image).filter(Image.id == id_).one().image
        session.commit()
        return resp

    def delete_image_by_id(self, id_: int):
        session = self._session_factory()
        session.query(Image).filter(Image.id == id_).delete()
        session.commit()

    def _delete_old_images(self):
        session = self._session_factory()
        session.query(Image) \
            .filter(
            ImageRepository.get_current_timestamp() - Image.timestamp >= 3000
        ) \
            .delete()

        session.commit()
