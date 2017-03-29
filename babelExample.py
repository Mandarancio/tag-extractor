#! /usr/bin/python3

import requests
import json
from babel import Babel


if __name__ == '__main__':
    babel = Babel()
    # Example for desambiguate a sentence
    sentence = "I bought a car"
    print(babel.desambiguate(sentence))
    # Example to get the sense of a word in a file
    word = "slowly"
    outputFile = "myFile.txt"
    babel.getSense(word, outputFile)
