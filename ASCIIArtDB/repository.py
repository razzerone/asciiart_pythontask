from datetime import datetime

import web_settings


class Repository:
    def add_image(self, image: bytes) -> int:
        raise NotImplementedError

    def get_image_by_id(self, id_: int) -> bytes:
        raise NotImplementedError

    @staticmethod
    def get_current_timestamp() -> int:
        return int(datetime.now().strftime(web_settings.datetime_format))
