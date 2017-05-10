#! /usr/bin/python3
"""
"""
# @Djavan Sergent
import tagextractor.storage.dbmanager as db
from sqlalchemy import Column, Integer, Sequence, String, exists
from sqlalchemy.orm import relationship


class Tag(db.Base):
    """
    A mapping class for Tag Objects
    """
    __tablename__ = "tag"

    # Table fields
    id = Column(Integer, Sequence('tag_id_seq'), primary_key=True)
    tag = Column(String, nullable=False)
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
