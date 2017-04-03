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

    # Table fields
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


class Tags(Base):
    __tablename__ = "tags"

    # Table fields
    id = Column(Integer, Sequence('pictures_id_seq'), primary_key=True)
    tag = Column(String, nullable=False)


def add_pict_to_db(picture, session):
    """
    :param picture: the picture to store
    :param session: database session
    """
    tags = ''
    for tag in picture['tags']:
        tags += tag['tag'] + " "

    pict = Pictures(pict=picture['id'], posted=picture['posted'], taken=picture['taken'],
                        tags=tags, ntags=len(picture['tags']), owner=picture['owner'],
                        lat=picture['lat'], lon=picture['lon'])
    session.add(pict)
    session.commit()  # not optimized !

def add_tag_to_db(tag, session):
    """
    :param tag: the picture to store
    :param session: database session
    """

    t = Tags(tag=tag)
    session.add(t)
    session.commit()
