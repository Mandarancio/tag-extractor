from nltk.corpus import wordnet as wn
from unidecode import unidecode


class Wordreader:
    def __init__(self):
        self.lemmas = []
        self.hypernyms = []

    def lemmatizer(self, photo):
        """
        :param photo: the photo we want to find lemmas
        :return: list of lemmas of the word
        """
        self.lemmas.clear()
        for tag in photo['tags']:
            synsets = wn.synsets(unidecode(tag['tag']))
            for s in synsets:
                name = s.name()
                lems = wn.synset(name).lemmas()
                for l in lems:
                    if l not in self.lemmas:
                        self.lemmas.append(l)
        return self.lemmas

    def hypernymizer(self, photo):
        self.hypernyms.clear()
        for lemma in photo['lemmas']:
            synsets = wn.synsets(lemma.name())
            for s in synsets:
                hyper = s.hypernyms()
                for h in hyper:
                    if h not in self.hypernyms:
                        self.hypernyms.append(h)
        return self.hypernyms
