#! /usr/bin/python3
"""Picture tag link database table manager
author: Djavan Sergent
"""
import tagextractor.classification.storage.base as db
from sqlalchemy import Column, Integer, ForeignKey


# pylint: disable = too-few-public-methods
class PictureCategoryLink(db.CLASSIFIED_BASE):
    """A mapping class for link between Picture and Category Object."""
    __tablename__ = 'picture_category_link'

    # Table fields
    category_id = Column(Integer, ForeignKey('category.id'), primary_key=True)
    picture_id = Column(Integer, ForeignKey('picture.id'), primary_key=True)

    def __repr__(self):
        """Print the picture tag link."""
        return "<Link(pid='%s', cid='%s')>" \
               % (self.picture_id, self.category_id)
