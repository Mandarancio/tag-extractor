#! /usr/bin/python3
"""Example of use  of the babel net api"""
from tagextractor.conceptualization.babel import Babel
import tagextractor.extraction.extractors as exs


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


if __name__ == '__main__':
    #Attention ne utilisant les requêtes babelfly/bablenet
    #le nombre est très limité pour l'instant!

    flickrKey = u'flickrKey'
    flickrSecretKey = u'flickSecretKey'
    babelKey = "babelKey"
    babel = Babel(babelKey)

    # Flickr Extractor
    f = exs.FlickrExtractor(flickrKey, flickrSecretKey)

    for i in babel.add_lemmas( f.get_tags(lat=46.205850, lon=6.157521,
                         radius=1, num_photos=1)):
        print(i)

    """
    # Example for desambiguate a sentence
    sentence = "I bought a car"
    print(babel.desambiguate(sentence))
    # Example to get the sense of a word in a file
    word = "slowly"
    outputFile = "myFile.txt"
    babel.get_sense(word, outputFile)
    """
