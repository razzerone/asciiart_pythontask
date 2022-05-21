import datetime

from sqlalchemy import create_engine, Column, Integer, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

import web_settings

engine = create_engine(web_settings.db)
Base = declarative_base()


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    image = Column(LargeBinary)
    timestamp = Column(Integer)

    def __init__(self, image: bytes):
        super().__init__()
        self.image = image
        self.timestamp = int(
            datetime.datetime.now().strftime(web_settings.datetime_format)
        )
