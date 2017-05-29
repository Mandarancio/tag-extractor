#! /usr/bin/python3
"""Picture Database table.
author: Djavan Sergent
"""
import tagextractor.classification.storage.base as db
from tagextractor.classification.storage.models.tag import Tag
from tagextractor.classification.storage.models.category import Category
from sqlalchemy import Column, Integer, Float, String, Sequence, exists
from sqlalchemy.orm import relationship


class Picture(db.CLASSIFIED_BASE):
    """A Mapping class for Picture Objects."""
    __tablename__ = 'picture'

    # Table fields
    # pylint: disable=invalid-name
    id = Column(Integer, Sequence('pictures_id_seq'), primary_key=True)
    pict = Column(String, nullable=False)
    posted = Column(String)
    taken = Column(String)
    ntags = Column(Integer, nullable=False)
    owner = Column(String)
    url = Column(String)
    image_url = Column(String)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    categories = relationship(Category, secondary='picture_category_link')
    tags = relationship(Tag, secondary='picture_tag_link')

    # Bind tags to picture and picture to tags
    def add_tags(self, tags, session):
        """Add tags to dB."""
        # List of picture's tags
        ptags = []
        for ptag in tags:
            ptags.append(ptag['tag_id'])

        # Tag request, filtered on ptags
        tags = session.query(Tag).filter(Tag.tag_id.in_(ptags))
        # Binding
        for tag in tags:
            self.tags.append(tag)
            tag.pictures.append(self)

    # Bind tags to picture and picture to tags
    def add_categories(self, categories, session):
        """Add tags to dB."""
        # List of picture's tags
        categs = []
        for category in categories:
            categs.append(category.name)

        # Tag request, filtered on ptags
        categs = session.query(Category).filter(Category.name.in_(categs))
        # Binding
        for categ in categs:
            self.categories.append(categ)
            categ.pictures.append(self)

    # Test of existance in database
    def exist(self, session):
        """
        :param session: database transaction session
        :return: Boolean - False if not in database
        """
        return session.query(exists().where(
            Picture.pict == self.pict)).scalar()

    def __repr__(self):
        """Print the picture."""
        return "<Picture(id='%s', pict='%s', lat='%s', lon='%s')>" \
               % (self.id, self.pict, self.lat, self.lon)
