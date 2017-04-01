#! /usr/bin/python3
import sqlmanager as sql

# Checking the database content
# @Djavan Sergent
if __name__ == "__main__":
    session = sql.Session()

    picts = session.query(sql.Pictures).order_by(sql.Pictures.id)

    for pict in picts:
        print(pict)
