class Repository:
    def add_image(self, image: bytes) -> int:
        raise NotImplementedError

    def get_image_by_id(self, id_: int) -> bytes:
        raise NotImplementedError
