#! /usr/bin/python3
# See http://docs.sqlalchemy.org/en/latest/orm/tutorial.html for more details about SQLAlchemy
from sqlalchemy import Column, Integer, Float, String, Sequence
import sqlmanager as sql


class Pictures(sql.Dbconfig().Base):
    """
    A Mapping class which link Database and Object pictures
    @Djavan Sergent
    """
    __tablename__ = 'pictures'

    # Table field
    id = Column(Integer, Sequence('pictures_id_seq'), primary_key=True)
    pict = Column(String, nullable=False)
    posted = Column(String)
    taken = Column(String)
    tags = Column(String, nullable=False)
    ntags = Column(Integer, nullable=False)
    owner = Column(String)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)

    def __repr__(self):
        return "<Picture(id='%s', pict='%s', tags='%s', lat='%s', lon='%s')>" \
               % (self.id, self.pict, self.tags, self.lat, self.lon)
