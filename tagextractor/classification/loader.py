"""Simple JSON/DB loader."""
from sqlalchemy import func

import tagextractor.storage.dbmanager as dbm
from tagextractor.storage.base import BASE
from tagextractor.storage.models.picture import Picture


class Loader:
    """Base class of loader."""
    def __init__(self, source):
        """Abstract initilaizer.

        Args
        ----
            source: file origin.
        """
        self.source = source

    def load(self, number=-1):
        """Loads photo and tags method.

        Args
        ----
            number: number of photos to load, if -1 all

        Returns
        -------
            photos and tags structure

        """
        pass

    def photo_number(self):
        """Returns the number of photos in the file.

        Returns
        -------
            number of photos

        """
        pass


def __dbtag_to_dictag__(tag):
    dictag = {
        "tag": tag.tag,
        "raw": tag.raw,
        "tag_id": tag.tag_id,
        "lemma": tag.lemma,
        "synset": tag.synset
    }
    return dictag


def __dbpic_to_dicpic__(pic):
    dicpic = {
        "name": pic.pict,
        "lat": pic.lat,
        "lon": pic.lon,
        "posted": pic.posted,
        "taken": pic.taken,
        "owner": pic.owner,
        "tags": []
    }
    for tag in pic.tags:
        dicpic['tags'].append(__dbtag_to_dictag__(tag))

    return dicpic


class DBLoader(Loader):
    """sqlite loader."""
    def __init__(self, source):
        """Initialize the sqlite senssion."""
        Loader.__init__(self, source)
        self.manager = dbm.DBManager(source)
        BASE.metadata.create_all(self.manager.engine())
        self.session = self.manager.session()

    def load(self, number=-1):
        """Yield N pictures."""
        photos = self.session.query(Picture)
        counter = 0
        for pic in photos:
            yield __dbpic_to_dicpic__(pic)
            counter += 1
            if number > 0 and counter >= number:
                break

    def photo_number(self):
        """Return the number of photo stored."""
        return self.session.query(func.count(Picture.id))[0][0]


if __name__ == '__main__':
    LOADER = DBLoader("sqlite:///database/synx_instagram.db")
    print(LOADER.photo_number())
    for photo in LOADER.load(2):
        print(photo)
