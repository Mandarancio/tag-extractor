#! /usr/bin/python3
import re
from nltk import FreqDist
from nltk.corpus import brown
from nltk.corpus import words


def pprint(tree, space=''):
    if tree is None:
        return
    for l in tree:
        print(space+l['term']+'('+str(l['freq'])+')')
        pprint(l['rest'], '  '+space)


class SimpleSplitter:
    def parseTag(self, term):
        words = []
        # Remove hashtag, split by dash
        term = term.replace('-', ' ').replace('_', ' ').replace('+', ' ')
        tags = re.sub(r"([A-Z])", r" \1", term).split()
        return tags


class HashtagSplitter:
    def __init__(self):
        self.__frequency_list__ = FreqDist(i.lower() for i in brown.words())
        self.__words__ = words.words()

    def parseTag(self, term):
        words = []
        # Remove hashtag, split by dash
        term = term.replace('-', ' ').replace('_', ' ').replace('+', ' ')
        tags = re.sub(r"([A-Z])", r" \1", term).split()
        for tag in tags:
            if len(tag) <= 2:
                words.append(tag)
            else:
                res = self.recursiveParse(tag)
                prob, extracted = self.__max__(res)
                # pprint(res)
                words.extend(extracted)
        return words

    def recursiveParse(self, term):
        if len(term) == 1:
            return [{'term': term, 'freq': self.freq(term), 'rest': None}]
        reslist = []
        for i in range(1, len(term)+1):
            if self.findWord(term[0:i]):
                res = {}
                if i < len(term):
                    res['term'] = term[0:i]
                    res['freq'] = self.freq(term[0:i])
                    res['rest'] = self.recursiveParse(term[i:])
                else:
                    res['term'] = term
                    res['freq'] = self.freq(term)
                    res['rest'] = None
                reslist.append(res)
        if len(reslist) == 0:
            return [{'term': term, 'freq': 0, 'rest': None}]
        return reslist

    def __max__(self, l):
        if l is None:
            return 1, []
        max_i = 0
        max_score = l[0]['freq']
        max_path = []
        if l[0]['rest'] is not None:
            ms, path = self.__max__(l[0]['rest'])
            max_score *= ms
            max_path = path
        for i in range(1, len(l)):
            score = l[i]['freq']
            path = []
            if l[i]['rest'] is not None:
                ms, path = self.__max__(l[i]['rest'])
                score *= ms
            if score > max_score:
                max_score = score
                max_i = i
                max_path = path
        path = [l[max_i]['term']]
        path.extend(max_path)
        return max_score, path

    def freq(self, word):
        return self.__frequency_list__.freq(word)

    def findWord(self, token):
        return token in self.__words__


if __name__ == "__main__":
    splitter = HashtagSplitter()
    print('loaded')
    hashtag = 'awesomedayofmylife'
    hashtag = 'ilovegeneva'
    print('Hashtag: '+hashtag)
    print(splitter.parseTag(hashtag))
    hashtag = "ILoveGeneva"
    print('Hashtag: '+hashtag)
    simple = SimpleSplitter()
    print(simple.parseTag(hashtag))
