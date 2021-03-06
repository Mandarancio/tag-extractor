#! /usr/bin/python3
"""Picture Database table.
author: Djavan Sergent
"""
import tagextractor.storage.base as db
from tagextractor.storage.models.tag import Tag
from sqlalchemy import Column, Integer, Float, String, Sequence, exists
from sqlalchemy.orm import relationship


class Picture(db.BASE):
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
    tags = relationship(Tag, secondary='picture_tag_link')

    # Bind tags to picture and picture to tags
    def add_tags(self, tags, session):
        """Add tags to dB."""
        # List of picture's tags
        ptags = []
        for ptag in tags:
            if ptag['lemmas']:
                for i in range(0, len(ptag['lemmas'])):
                    tid = '{}#{}'.format(ptag['id'], i)
                    ptags.append(tid)
            else:
                ptags.append(ptag['id'])

        # Tag request, filtered on ptags
        tags = session.query(Tag).filter(Tag.tag_id.in_(ptags))
        # Binding
        for tag in tags:
            self.tags.append(tag)
            tag.pictures.append(self)

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
