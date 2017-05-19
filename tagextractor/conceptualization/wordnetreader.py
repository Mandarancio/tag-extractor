#! /usr/bin/python3
"""WordNet utils.

author: Djavan Sergent
"""
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
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

    def extract(self, photos):
        """Extract Lemmas and synset from each photo."""
        for photo in photos:
            yield self.tag_expanser(photo)

    def tag_expanser(self, photo):
        """
        :param photo: the photo we want to expanse tags information
        """
        sentence = ''
        for tag in photo['tags']:
            sentence += unidecode(tag['raw'])+' '
        i = 0
        for tag in photo['tags']:
            photo['tags'][i]['lemmas'] = []
            photo['tags'][i]['synsets'] = []
            for word in tag['raw'].split():
                lemmas, synsets = self.__lemmatizer__(word, sentence)
                if lemmas:
                    photo['tags'][i]['lemmas'].append(lemmas)
                    photo['tags'][i]['synsets'].append(synsets)
            i += 1
        return photo

    # pylint: disable=R0201
    def __lemmatizer__(self, tag, sentence):
        """
        :param tag: the tag we want to find lemmas
        :return: a list of lemmas
        """

        synsets = lesk(sentence, unidecode(tag))
        if synsets:
            syns = synsets.name()
            lemma = synsets.lemmas()[0].name()
            return lemma, syns
        return None, None


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
