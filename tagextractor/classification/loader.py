"""Simple JSON/DB loader."""
import re
from sqlalchemy import func

import tagextractor.storage.dbmanager as dbm
from tagextractor.storage.base import BASE
from tagextractor.storage.models.picture import Picture


def __clean__(word):
    """Simply remove all trash characters."""
    return re.sub('[^A-Za-z0-9. ]+', '', word)


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
        "tag": __clean__(tag.tag),
        "raw": __clean__(tag.raw),
        "tag_id": __clean__(tag.tag_id),
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
        "url": pic.url,
        "image_url": pic.image_url,
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
    for photo in LOADER.load(10):
        print(photo['tags'])
