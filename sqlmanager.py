#! /usr/bin/python3
# See http://docs.sqlalchemy.org/en/latest/orm/tutorial.html for more details about SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class Dbconfig():
    def __init__(self):
        self.Base = declarative_base()
        self.engine = create_engine('sqlite:///../database/kr.bd', echo=False)  # echo = logging in console
        self.Session = sessionmaker(bind=self.engine)
