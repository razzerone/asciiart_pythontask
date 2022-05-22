from sqlalchemy import create_engine, Column, Integer, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

import web_settings

engine = create_engine(web_settings.db, echo=True)
Base = declarative_base()


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    image = Column(LargeBinary)
    timestamp = Column(Integer)

    def __repr__(self):
        return f'<Image(id={self.id}>)'
