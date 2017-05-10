#! /usr/bin/python3
"""DB manager using SQLAlchemy.

See http://docs.sqlalchemy.org/en/latest/orm/tutorial.html for more
details about SQLAlchemy.

author: Djavan Sergent
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Classes which needed a Base, no on top import
from tagextractor.models.tag import Tag
from tagextractor.models.picture import Picture
# Used for table creation ! do not delete this line !
# from tagextractor.models.picturetaglink import PictureTagLink

# Database engine and session parameters
BASE = declarative_base()
# echo = logging in console
ENGINE = create_engine('sqlite:///../database/kr2.db', echo=False)
SESSION = sessionmaker(bind=ENGINE)


def add_pict_to_db(picture, session):
    """
    :param picture: the picture to store
    :param session: database transaction session
    """
    pict = Picture(pict=picture['id'], posted=picture['posted'],
                   taken=picture['taken'],
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
    tag = Tag(tag=tag)
    if not tag.exist(session):
        session.add(tag)
