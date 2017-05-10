#! /usr/bin/python3
"""WordNet utils.

author: Djavan Sergent
"""
from nltk.corpus import wordnet as wn
from unidecode import unidecode


class Wordnetreader:
    """
    A class which explore the WordNet graph with NLTK package
    @Djavan Sergent
    """
    def __init__(self):
        self.langs = ["eng"]

    def avaible_langs(self):
        """return avaible langs"""
        return self.langs

    def tag_expanser(self, photo):
        """
        :param photo: the photo we want to expanse tags information
        """
        i = 0
        for tag in photo['tags']:
            photo['tags'][i]['lemmas'] = self.__lemmatizer__(tag['tag'])
            photo['tags'][i]['hypernyms'] = \
                __hypernymizer__(photo['tags'][i]['lemmas'])
            i += 1

    def __lemmatizer__(self, tag):
        """
        :param tag: the tag we want to find lemmas
        :return: a list of lemmas
        """
        lemmas = []
        synsets = []
        for lang in self.langs:
            synsets += wn.synsets(tag, lang=lang)
            synsets += wn.synsets(unidecode(tag), lang=lang)
        for synset in synsets:
            lems = self.__get_lemmas__(synset)
            for lemma in lems:
                if lemma.name() not in lemmas:
                    lemmas.append(lemma.name())
        return lemmas

    def __get_lemmas__(self, synset):
        """
        :param synset: synset from which lemmas are extracted
        :return: list of lemmas
        """
        word = synset.name()
        synsets = []
        for lan in self.langs:
            synsets += wn.synset(word).lemmas(lang=lan)
        return synsets


def __hypernymizer__(lemmas):
    """
    :param lemmas: list of lemmas to extract hypernyms
    :return: a list of hypernyms
    """
    hypernyms = []
    for lemma in lemmas:
        synsets = wn.synsets(lemma)
        for syn in synsets:
            hypers = syn.hypernyms()
            for hyper in hypers:
                if hyper.name() not in hypernyms:
                    hypernyms.append(hyper.name())
    return hypernyms
