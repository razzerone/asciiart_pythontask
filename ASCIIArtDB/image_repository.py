from datetime import datetime

import web_settings


class ImageRepository:
    """Интерфейс временного хранения изображений."""

    def add_image(self, image: bytes) -> int:
        """Добавление изображения в базу данных."""
        raise NotImplementedError

    def get_image_by_id(self, id_: int) -> bytes:
        """Получение изображения из базы данных по id."""
        raise NotImplementedError

    def delete_old_images(self):
        """
        Удаляет изображения, которые хранятся дольше, чем указан image_ttl
        в web_settings.py
        """
        raise NotImplementedError

    @staticmethod
    def get_current_timestamp() -> int:
        """Получение текущего времени в формате, указанном в web_settings.py"""
        return int(datetime.now().strftime(web_settings.datetime_format))
