#! /usr/bin/python3
# Martino Ferrari
import re
import time
import json


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
    '''
    High-perforamnce Advanced hashtag splitter using frequency of possible word
    combination to split correctly the tag.
    @Martino Ferrari
    :param freq_file: json frequency wordlist
    '''
    def __init__(self, freq_file):
        fp = open(freq_file)
        self.__freqs__ = json.load(fp)
        fp.close()

    def parse_tag(self, term):
        '''
        parse a tag, first step use standarad delimiter, numbers to split
        then it use the frequency
        :param term: tag to parse (no hash please)
        :return: tag splitted in a list
        '''
        words = []
        # Remove hashtag, split by dash
        term = term.replace('-', ' ').replace('_', ' ').replace('+', ' ')
        tags = re.sub(r"([0-9]+)", r" \1 ", term).split()
        for tag in tags:
            if len(tag) <= 2 or len(tag) > 20:
                words.append(tag.lower())
            else:
                _, res = self.recursive_split(tag.lower())
                words.extend(res)
        return words

    def recursive_split(self, term):
        '''
        this is the actual magic of the class ;)
        :param term: all low case tag to split
        :return: most probable bag of words
        '''
        max_freq = self.freq(term)
        res = [term]
        for i in range(len(term), 0, -1):
            word = term[0:i]
            ff = self.freq(word)
            if ff > 0:
                fr, rest = self.recursive_split(term[i:])
                ff = ff*fr/2
                if ff > max_freq:
                    max_freq = ff
                    res = [word]
                    res.extend(rest)
        return max_freq, res

    def freq(self, word):
        '''
        return the frequency of a word
        :param word: word to check
        :return: frequency (0 if not in dictionary)
        '''
        if word not in self.__freqs__:
            return 0
        return self.__freqs__[word]

    def find_word(self, word):
        '''
        check if a word is the dictionary
        :param word: word to check
        :return: boolean
        '''
        return word in self.__freqs__


if __name__ == "__main__":
    def test(tag):
        print('Hashtag: '+tag)
        t = time.time()
        print(splitter.parse_tag(tag))
        t = time.time()-t
        print(t)

    splitter = HashtagSplitter('resources/freqs.json')
    print('loaded')
    test('makeupartist')
    test('awesome-dayofmylife')
    test('awesomedayofmylife')
    test('ilovegeneva')
    hashtag = "ILoveGeneva"
    print('Hashtag: '+hashtag)
    simple = SimpleSplitter()
    print(simple.parse_tag(hashtag))
    test('ILoveGeneva')
