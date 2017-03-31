#! /usr/bin/python3
import extractors as exs
import wordnetreader as wrd
import sqlmanager as sql


def printer(photo):
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
        if len(photo['tags']) > 0:
            w.tag_expanser(photo)
            string = printer(photo)

            # Database entry management
            db.add_to_db(photo, session)

            yield string
        else:
            yield ' - '+photo['id']+' ['+photo['lat']+', '+photo['lon']+']'


if __name__ == '__main__':
    # please do not publish it on github
    apikey = u'KEY_HERE'
    secret = u'SECRET_HERE'

    # Database management
    db = sql.Dbconfig()
    db.Base.metadata.create_all(db.engine)
    session = db.Session()

    # Wordnet Reader
    w = wrd.Wordnetreader()

    # Flickr Extractor
    f = exs.FlickrExtractor(apikey, secret)
    pipeline = prettifier(f.get_tags(lat=46.205850, lon=6.157521,
                                     radius=1, num_photos=50))

    for pretty in pipeline:
        print(pretty)
