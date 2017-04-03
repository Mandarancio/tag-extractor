#! /usr/bin/python3
# @Djavan Sergent
import dbmanager as db
from sqlalchemy import Column, Integer, Float, String, Sequence, exists
from sqlalchemy.orm import relationship
from models.tag import Tag


class Picture(db.Base):
    """
    A Mapping class for Picture Objects
    """
    __tablename__ = 'picture'

    # Table fields
    id = Column(Integer, Sequence('pictures_id_seq'), primary_key=True)
    pict = Column(String, nullable=False)
    posted = Column(String)
    taken = Column(String)
    ntags = Column(Integer, nullable=False)
    owner = Column(String)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    tags = relationship(Tag, secondary='picture_tag_link')

    # Bind tags to picture and picture to tags
    def add_tags(self, tags, session):

        # List of picture's tags
        ptags = []
        for ptag in tags:
            ptags.append(ptag['tag'])

        # Tag request, filtered on ptags
        tags = session.query(Tag).filter(Tag.tag.in_(ptags))

        # Binding
        for t in tags:
            self.tags.append(t)
            t.pictures.append(self)

    # Test of existance in database
    def exist(self, session):
        """
        :param session: database transaction session
        :return: Boolean - False if not in database
        """
        return session.query(exists().where(Picture.pict == self.pict)).scalar()

    def __repr__(self):
        return "<Picture(id='%s', pict='%s', lat='%s', lon='%s')>" \
               % (self.id, self.pict, self.lat, self.lon)
