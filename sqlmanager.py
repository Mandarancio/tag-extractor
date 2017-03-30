#! /usr/bin/python3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Pictures(Base):
    """
    @Djavan Sergent
    """
    __tablename__ = 'pictures'

    id = Column(Integer, primary_key=True)
    tags = Column(String)
    location = Column(String)

    def __repr__(self):
        return "<TAGS(id='%s', tags='%s', location='%s')>" %(self.id, self.tags, self.location)