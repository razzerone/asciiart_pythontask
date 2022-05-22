import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker

from ASCIIArtDB.tables import Image
from ASCIIArtDB.image_repository import ImageRepository


class ImageRepositoryImpl(ImageRepository):
    def __init__(self, engine=None):
        self._engine = engine
        self._session_factory = sessionmaker(bind=engine)

    def add_image(self, img_bin: bytes) -> int:
        with self._session_factory() as session:
            image = Image(
                image=img_bin,
                timestamp=ImageRepositoryImpl.get_current_timestamp()
            )
            session.add(image)
            session.commit()
            return image.id

    def get_image_by_id(self, id_: int) -> bytes | None:
        with self._session_factory() as session:
            try:
                resp = session\
                    .query(Image.image)\
                    .filter(Image.id == id_)\
                    .one()\
                    .image
                return resp
            except sqlalchemy.exc.NoResultFound:
                return None
            finally:
                session.commit()

    def delete_image_by_id(self, id_: int):
        with self._session_factory() as session:
            session.query(Image).filter(Image.id == id_).delete()
            session.commit()

    def delete_old_images(self):
        with self._session_factory() as session:
            session.query(Image) \
                .filter(
                ImageRepository.get_current_timestamp() - Image.timestamp >= 1000
            ) \
                .delete()

            session.commit()
