#! /usr/bin/python3
from nltk.corpus import wordnet as wn
from unidecode import unidecode


class Wordreader:
    def __init__(self):
        pass

    def rqst(self, word):
        uni_word = unidecode(word)
        synsets = wn.synsets(uni_word)
        for s in synsets:
            name = s.name()
            lemmas = wn.synset(name).lemmas()
            print(lemmas)
