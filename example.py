#! /usr/bin/python3
import extractors as exs
import wordreader as wrd


def printer(photo):
    string = ' + ' + photo['id'] + ' [' + photo['lat'] + ', ' + photo['lon'] + ']:\n'
    string += "\tTAGS : [  "
    for tag in photo['tags']:
        string += tag['tag'] + "\t"
    string += "]\n\tLEMMAS : [ "
    for lemma in photo['concepts']['lemmas']:
        string += lemma.name() + "\t"
    string += "]\n\tHYPERNYMS : [ "
    for hyper in photo['concepts']['hypernyms']:
        string += hyper.name() + "\t"
    string += "]"
    return string


def prettifier(photos):
    '''
    simple function to explain the use of a Pipeline
    :photos: list of extracted photos
    :return: list of pretty strings
    '''
    for photo in photos:
        if len(photo['tags']) > 0:
            photo['concepts'] = dict()
            photo['concepts']['lemmas'] = w.lemmatizer(photo)
            photo['concepts']['hypernyms'] = w.hypernymizer(photo)
            string = printer(photo)

            yield string
        else:
            yield ' - '+photo['id']+' ['+photo['lat']+', '+photo['lon']+']'

if __name__ == '__main__':
    # please do not publish it on github
    apikey = u'KEY_HERE'
    secret = u'SECRET_HERE'

    w = wrd.Wordreader()
    f = exs.FlickrExtractor(apikey, secret)
    pipeline = prettifier(f.get_tags(lat=46.205850, lon=6.157521,
                                     radius=1, num_photos=50))

    for pretty in pipeline:
        print(pretty)
