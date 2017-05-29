#! /usr/bin/python3
"""DB manager using SQLAlchemy.

See http://docs.sqlalchemy.org/en/latest/orm/tutorial.html for more
details about SQLAlchemy.

author: Djavan Sergent
"""

from sqlalchemy.ext.declarative import declarative_base

CLASSIFIED_BASE = declarative_base()
