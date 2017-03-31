#! /usr/bin/python3
# See http://docs.sqlalchemy.org/en/latest/orm/tutorial.html for more details about SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import models.pictures as pic


class Dbconfig():
    def __init__(self):
        self.Base = declarative_base()
        self.engine = create_engine('sqlite:///../database/kr.db', echo=False)  # echo = logging in console
        self.Session = sessionmaker(bind=self.engine)

    def add_to_db(self, picture, session):
        tags = ''
        for tag in picture['tags']:
            tags += tag['tag'] + " "

        pict = pic.Pictures(pict=picture['id'], posted=picture['posted'], taken=picture['taken'],
                            tags=tags, ntags=len(picture['tags']), owner=picture['owner'],
                            lat=picture['lat'], lon=picture['lon'])
        session.add(pict)
        session.commit()  # not optimized !
