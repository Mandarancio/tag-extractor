#! /usr/bin/python3
"""Picture tag link database table manager
author: Djavan Sergent
"""
import tagextractor.classification.storage.base as db
from sqlalchemy import Column, Integer, ForeignKey


# pylint: disable = too-few-public-methods
class PictureTagLink(db.CLASSIFIED_BASE):
    """A mapping class for link between Picture and Tag Object."""
    __tablename__ = 'picture_tag_link'

    # Table fields
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)
    picture_id = Column(Integer, ForeignKey('picture.id'), primary_key=True)

    def __repr__(self):
        """Print the picture tag link."""
        return "<Link(pid='%s', tid='%s')>" \
               % (self.picture_id, self.tag_id)
