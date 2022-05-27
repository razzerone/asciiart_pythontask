import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker

import web_settings
from ASCIIArtDB.tables import Image
from ASCIIArtDB.image_repository import ImageRepository


class ImageRepositoryImpl(ImageRepository):
    """Реализация интерфейса ImageRepository через орм sqlalchemy"""
    def __init__(self, engine=None):
        self._engine = engine
        self._session_factory = sessionmaker(bind=engine)

    def add_image(self, img_bin: bytes) -> int:
        """Добавление изображения в базу данных."""
        with self._session_factory() as session:
            image = Image(
                image=img_bin,
                timestamp=ImageRepositoryImpl.get_current_timestamp()
            )
            session.add(image)
            session.commit()
            return image.id

    def get_image_by_id(self, id_: int) -> bytes | None:
        """Получение изображения из базы данных по id."""
        with self._session_factory() as session:
            resp = session \
                .query(Image.image) \
                .filter(Image.id == id_) \
                .one_or_none()
            session.commit()

            return None if resp is None else resp.image

    def delete_old_images(self):
        """
        Удаляет изображения, которые хранятся дольше, чем указан image_ttl
        в web_settings.py
        """
        with self._session_factory() as session:
            session.query(Image) \
                .filter(
                ImageRepository
                .get_current_timestamp() -
                Image.timestamp >= web_settings.image_ttl
            ) \
                .delete()

            session.commit()
