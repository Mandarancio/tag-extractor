#! /usr/bin/python3
"""Example for read a table from the DB"""
import tagextractor.storage.dbmanager as dbm

# Checking the database content
# @Djavan Sergent
if __name__ == "__main__":
    SQL = dbm.DBManager("sqlite:///../database/instagram.db")
    SESSION = SQL.session()

    # content = session.query(sql.Tag).order_by(sql.Tag.id)
    CONTENT = SESSION.query(dbm.PictureTagLink)
    for c in CONTENT:
        print(c)
