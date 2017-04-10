#! /usr/bin/python3

import requests
import json
import sys
from babel import Babel
import extractors as exs
import wordnetreader as wrd


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

#Attention ne utilisant les requêtes babelfly/bablenet
#le nombre est très limité pour l'instant!
if __name__ == '__main__':

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
