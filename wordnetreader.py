#! /usr/bin/python3
from nltk.corpus import wordnet as wn
from unidecode import unidecode


class Wordnetreader:
    """
    A class which explore the WordNet graph with NLTK package
    @Djavan Sergent
    """
    def __init__(self):
        self.lemmas = []
        self.hypernyms = []

    def tag_expanser(self, photo):
        """
        :param photo: the photo we want to expanse tags information
        """
        i = 0
        for tag in photo['tags']:
            photo['tags'][i]['lemmas'] = self.__lemmatizer__(tag['tag'])
            photo['tags'][i]['hypernyms'] = self.__hypernymizer__(photo['tags'][i]['lemmas'])
            i += 1

    def __lemmatizer__(self, tag):
        """
        :param tag: the tag we want to find lemmas
        :return: a list of lemmas
        """
        self.lemmas.clear()
        synsets = wn.synsets(unidecode(tag))
        for s in synsets:
            lems = self.__get_lemmas__(s)
            for l in lems:
                if l.name() not in self.lemmas:
                    self.lemmas.append(l.name())
        return self.lemmas[:]

    def __get_lemmas__(self, synset):
        """
        :param synset: synset from which lemmas are extracted
        :return: list of lemmas
        """
        word = synset.name()
        return wn.synset(word).lemmas()

    def __hypernymizer__(self, lemmas):
        """
        :param lemmas: list of lemmas to extract hypernyms
        :return: a list of hypernyms
        """
        self.hypernyms.clear()
        for lemma in lemmas:
            synsets = wn.synsets(lemma)
            for syn in synsets:
                hyper = syn.hypernyms()
                for h in hyper:
                    if h.name() not in self.hypernyms:
                        self.hypernyms.append(h.name())
        return self.hypernyms[:]
