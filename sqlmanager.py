#! /usr/bin/python3
# @Djavan Sergent
# See http://docs.sqlalchemy.org/en/latest/orm/tutorial.html for more details about SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, Integer, Float, String, Sequence, ForeignKey, exists


# Database engine and session parameters
Base = declarative_base()
engine = create_engine('sqlite:///../database/kr.db', echo=False)  # echo = logging in console
Session = sessionmaker(bind=engine)


class Tag(Base):
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


class Picture(Base):
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


class PictureTagLink(Base):
    """
    A mapping class for link between Picture and Tag Object
    """
    __tablename__ = 'picture_tag_link'

    # Table fields
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)
    picture_id = Column(Integer, ForeignKey('picture.id'), primary_key=True)

    def __repr__(self):
        return "<Link(pid='%s', tid='%s')>" \
               % (self.picture_id, self.tag_id)


def add_pict_to_db(picture, session):
    """
    :param picture: the picture to store
    :param session: database transaction session
    """
    pict = Picture(pict=picture['id'], posted=picture['posted'], taken=picture['taken'],
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
    t = Tag(tag=tag)
    if not t.exist(session):
        session.add(t)
