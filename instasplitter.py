#! /usr/bin/python3
import re
from nltk import FreqDist
from nltk.corpus import brown
# from nltk.corpus import words
import time


def pprint(tree, space=''):
    if tree is None:
        return
    for l in tree:
        print(space+l['term']+'('+str(l['freq'])+')')
        pprint(l['rest'], '  '+space)


class SimpleSplitter:
    def parse_tag(self, term):
        '''
        Simple Splitter based on capitals, dash and underscores.
        :param term: tag to split
        :return: array of splitted words
        '''
        words = []
        # Remove hashtag, split by dash
        term = term.replace('-', ' ').replace('_', ' ').replace('+', ' ')
        tags = re.sub(r"([A-Z])", r" \1", term).split()
        return tags


class HashtagSplitter:
    def __init__(self):
        self.__frequency_list__ = FreqDist(i.lower() for i in brown.words())
        self.__most_10000__ = self.__to_dic__(
            self.__frequency_list__.most_common(100000))
        # self.__words__ = words.words()

    def __to_dic__(self, freqs):
        res = {}
        tot = 0
        for l in freqs:
            if len(l[0]) > 1:
                res[l[0]] = l[1]
                tot += l[1]
            elif l[0] == 'a' or l[0] == 'i':
                res[l[0]] = l[1]
                tot += l[1]
        for k in res:
            res[k] /= tot
        return res

    def parse_tag(self, term):
        words = []
        # Remove hashtag, split by dash
        term = term.replace('-', ' ').replace('_', ' ').replace('+', ' ')
        tags = re.sub(r"([0-9]+)", r" \1 ",
                      re.sub(r"([A-Z])", r" \1", term)).split()
        for tag in tags:
            if len(tag) <= 2 or len(tag) > 15:
                words.append(tag)
            else:
                _, res = self.recursive_split(tag.lower())
                words.extend(res)
        return words

    def recursive_split(self, term):
        if self.find_word(term):
            max_freq = self.freq(term)
        else:
            max_freq = 0
        res = [term]
        for i in range(len(term), 0, -1):
            word = term[0:i]
            if self.find_word(word):
                ff = self.freq(word)
                fr, rest = self.recursive_split(term[i:])
                ff = ff*fr/2
                if ff > max_freq:
                    max_freq = ff
                    res = [word]
                    res.extend(rest)
        return max_freq, res

    def freq(self, word):
        return self.__most_10000__[word]

    def find_word(self, token):
        return token in self.__most_10000__


def test(tag):
    print('Hashtag: '+tag)
    t = time.time()
    print(splitter.parse_tag(tag))
    t = time.time()-t
    print(t)


if __name__ == "__main__":
    splitter = HashtagSplitter()
    print('loaded')
    print('freq: makeup')
    print(splitter.freq('makeup'))
    print(splitter.freq('make')*splitter.freq('up'))
    test('makeupartist')
    test('awesomedayofmylife')
    test('ilovegeneva')
    hashtag = "ILoveGeneva"
    print('Hashtag: '+hashtag)
    simple = SimpleSplitter()
    print(simple.parse_tag(hashtag))
