#! /usr/bin/python3
# @Djavan Sergent
# See http://docs.sqlalchemy.org/en/latest/orm/tutorial.html for more details about SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Database engine and session parameters
Base = declarative_base()
engine = create_engine('sqlite:///../database/kr2.db', echo=False)  # echo = logging in console
Session = sessionmaker(bind=engine)

# Classes which needed a Base, no on top import
from models.tag import Tag
from models.picture import Picture
from models.picturetaglink import PictureTagLink  # Used for table creation ! do not delete this line !


def add_pict_to_db(picture, session):
    """
    :param picture: the picture to store
    :param session: database transaction session
    """
    pict = Picture(pict=picture['id'], posted=picture['posted'], taken=picture['taken'],
                   ntags=len(picture['tags']), owner=picture['owner'],
                   lat=picture['lat'], lon=picture['lon'])

    # If picture not in the database
    if not pict.exist(session):
        for ptag in picture['tags']:
            # add tags to the database
            add_tag_to_db(ptag['tag'], session)

        # Picture added to session
        session.add(pict)

        # session flush : all elements inserted into database
        session.commit()

        # add tags to pictures and pictures to tags (links)
        pict.add_tags(picture['tags'], session)

        # Session flush : validation of links
        session.commit()


def add_tag_to_db(tag, session):
    """
    :param tag: the tag to store
    :param session: database transaction session
    """
    t = Tag(tag=tag)
    if not t.exist(session):
        session.add(t)
