#! /usr/bin/python3
# See http://docs.sqlalchemy.org/en/latest/orm/tutorial.html for more details about SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, Float, String, Sequence

Base = declarative_base()
engine = create_engine('sqlite:///../database/kr.db', echo=False)  # echo = logging in console
Session = sessionmaker(bind=engine)


class Pictures(Base):
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


def add_to_db(picture, session):
    tags = ''
    for tag in picture['tags']:
        tags += tag['tag'] + " "

    pict = Pictures(pict=picture['id'], posted=picture['posted'], taken=picture['taken'],
                        tags=tags, ntags=len(picture['tags']), owner=picture['owner'],
                        lat=picture['lat'], lon=picture['lon'])
    session.add(pict)
    session.commit()  # not optimized !