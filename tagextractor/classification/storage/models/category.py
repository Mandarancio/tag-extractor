#! /usr/bin/python3
"""CATEGORY Table DB manager.

author: Djavan Sergent
"""
import tagextractor.classification.storage.base as db
from sqlalchemy import Column, Integer, Sequence, String, exists
from sqlalchemy.orm import relationship


# pylint: disable=too-few-public-methods
class Category(db.CLASSIFIED_BASE):
    """A mapping class for Category Objects."""
    __tablename__ = "category"

    # Table fields
    # pylint: disable=invalid-name
    id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name = Column(String, nullable=False)

    pictures = relationship('Picture', secondary='picture_category_link')

    def exist(self, session):
        """
        :param session: database transaction session
        :return: Boolean - False if not in database
        """
        return session.query(exists().where(
            Category.name == self.name)).scalar()

    def __repr__(self):
        """Print the category."""
        return "<Category(id='%s', name='%s')>" \
               % (self.id, self.name)
