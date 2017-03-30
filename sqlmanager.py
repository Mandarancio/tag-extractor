#! /usr/bin/python3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Sequence, create_engine

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)


class Pictures(Base):
    """
    @Djavan Sergent
    """
    __tablename__ = 'pictures'

    id = Column(Integer, Sequence('pictures_id_seq'), primary_key=True)
    pict = Column(String)
    tags = Column(String)
    location = Column(String)

    def __repr__(self):
        return "<Picture(id='%s', pict='%s', tags='%s', location='%s')>" %(self.id, self.pict, self.tags, self.location)