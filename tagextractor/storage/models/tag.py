#! /usr/bin/python3
"""TAG Table DB manager.

author: Djavan Sergent
"""
import storage.base as db
from sqlalchemy import Column, Integer, Sequence, String, exists
from sqlalchemy.orm import relationship


class Tag(db.BASE):
    """
    A mapping class for Tag Objects
    """
    __tablename__ = "tag"

    # Table fields
    id = Column(Integer, Sequence('tag_id_seq'), primary_key=True)
    tag = Column(String, nullable=False)
    raw = Column(String, nullable=False)
    tag_id = Column(String, nullable=False)
    lemma = Column(String)
    synset = Column(String)
    pictures = relationship('Picture', secondary='picture_tag_link')

    def exist(self, session):
        """
        :param session: database transaction session
        :return: Boolean - False if not in database
        """
        return session.query(exists().where(Tag.tag == self.tag)).scalar()

    def __repr__(self):
        return "<Tag(id='%s', tag='%s')>" \
               % (self.id, self.tag)
