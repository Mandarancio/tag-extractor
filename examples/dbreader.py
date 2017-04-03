#! /usr/bin/python3
import sqlmanager as sql

# Checking the database content
# @Djavan Sergent
if __name__ == "__main__":
    session = sql.Session()

    # content = session.query(sql.Tag).order_by(sql.Tag.id)
    content = session.query(sql.PictureTagLink)
    for c in content:
        print(c)
