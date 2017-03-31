#! /usr/bin/python3
import sqlmanager as sql
import models.pictures as pic

# Checking the database content
# @Djavan Sergent
if __name__ == "__main__":
    session = sql.Dbconfig().Session()

    picts = session.query(pic.Pictures).order_by(pic.Pictures.id)

    for pict in picts:
        print(pict)
