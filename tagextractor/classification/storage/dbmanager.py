#! /usr/bin/python3
"""DB manager using SQLAlchemy.

See http://docs.sqlalchemy.org/en/latest/orm/tutorial.html for more
details about SQLAlchemy.

author: Djavan Sergent
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Classes which needed a Base, no on top import
from tagextractor.classification.storage.models.tag import Tag
from tagextractor.classification.storage.models.picture import Picture

# Used for table creation ! do not delete these lines !
# pylint: disable = unused-import
from tagextractor.classification.storage.models.picturetaglink import PictureTagLink
from tagextractor.classification.storage.models.picturecategorylink import PictureCategoryLink


class DBManager:
    """DB manager"""
    def __init__(self, path):
        """Initialize database manager."""
        # Database engine and session parameters
        # echo = logging in console
        self.__engine__ = create_engine(path, echo=False)
        self.__session__ = sessionmaker(bind=self.__engine__)

    def engine(self):
        """Get engine"""
        return self.__engine__

    def session(self):
        """Get session"""
        return self.__session__()

    def close(self):
        """Close sessions"""
        self.__session__.close_all()


def add_pict_to_db(picture, session):
    """
    :param picture: the picture to store
    :param session: database transaction session
    """
    pict = Picture(pict=picture['id'], posted=picture['posted'],
                   taken=picture['taken'],
                   ntags=len(picture['tags']), owner=picture['owner'],
                   lat=picture['lat'], lon=picture['lon'], categories=picture['categorie'])

    # If picture not in the database
    if not pict.exist(session):
        for ptag in picture['tags']:
            # add tags to the database
            __add_tag_to_db__(ptag, session)

        # Picture added to session
        session.add(pict)

        # session flush : all elements inserted into database
        session.commit()

        # add tags to pictures and pictures to tags (links)
        pict.add_tags(picture['tags'], session)

        # Session flush : validation of links
        session.commit()


def __add_tag_to_db__(tag, session):
    """
    :param tag: the tag to store
    :param session: database transaction session
    """
    if tag['lemmas']:
        for i in range(0, len(tag['lemmas'])):
            tid = '{}#{}'.format(tag['id'], i)
            ntag = Tag(tag=tag['tag'], raw=tag['raw'], tag_id=tid,
                       lemma=tag['lemmas'][i], synset=tag['synsets'][i], category=tag['category'])
        if not ntag.exist(session):
            session.add(ntag)
    else:
        tag = Tag(tag=tag['tag'], raw=tag['raw'], tag_id=tag['id'], category=tag['category'])
        if not tag.exist(session):
            session.add(tag)
