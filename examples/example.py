#! /usr/bin/python3
"""Example of wnet reader"""
import tagextractor.extraction.extractors as exs
import tagextractor.conceptualization.wordnetreader as wrd
import tagextractor.storage.dbmanager as db


def __printer__(photo):
    string = ' + ' + photo['id'] + ' [' + photo['lat'] + ', ' +\
            photo['lon'] + ']:\n'
    string += " TAGS : [\n"
    for tag in photo['tags']:
        string += "\t # " + tag['tag'] + "\n\t\t> LEMMAS : "
        for lemma in tag['lemmas']:
            string += "\t" + lemma + "\t"
        string += "\n\t\t> HYPERNYMS : "
        for hyper in tag['hypernyms']:
            string += "\t" + hyper + "\t"
        string += "\n"
    string += "]"
    return string


def prettifier(photos):
    """
    simple function to explain the use of a Pipeline
    :param photos: list of extracted photos
    :return: list of pretty strings
    """
    for photo in photos:
        if photo['tags']:
            w.tag_expanser(photo)
            string = __printer__(photo)

            # Database entry management
            db.add_pict_to_db(photo, session)

            yield string
        else:
            yield ' - '+photo['id']+' ['+photo['lat']+', '+photo['lon']+']'


if __name__ == '__main__':
    # please do not publish it on github
    apikey = u'KEY_HERE'
    secret = u'SECRET_HERE'

    # Création de la base de données (Tables)
    DB = db.DBManager("sqlite:///../database/instagram.db")
    # Database management
    session = DB.session()

    # Wordnet Reader
    w = wrd.Wordnetreader()

    # Flickr Extractor
    f = exs.FlickrExtractor(apikey, secret)
    pipeline = prettifier(f.get_tags(lat=46.205850, lon=6.157521,
                                     radius=1, num_photos=50))

    for pretty in pipeline:
        print(pretty)
