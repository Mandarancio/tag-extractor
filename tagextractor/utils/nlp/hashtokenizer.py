#! /usr/bin/python3
"""Hashtag tokenizer.

author: Martino Ferrari
"""
import re
import time
import json
import sys


def parse_tag(term):
    """
    Simple Splitter based on capitals, dash and underscores.

    @Martino Ferrari
    :param term: tag to split
    :return: array of splitted words
    """
    # Remove hashtag, split by dash
    term = term.replace('-', ' ').replace('_', ' ').replace('+', ' ')
    tags = re.sub(r"([A-Z])", r" \1", term).split()
    return tags


class HashTagTokenizer:
    """
    High-perforamnce Advanced hashtag tokenizerr using frequency of possible
    word combination to split correctly the tag.

    @Martino Ferrari
    :param freq_file: json frequency wordlist
    """
    def __init__(self, freq_file='resources/freqs.json'):
        """Initialize class."""
        with open(freq_file) as frequency_file:
            self.__freqs__ = json.load(frequency_file)

    def tokenize_tag(self, term):
        """
        Parse a tag, first step use standarad delimiter, numbers to split
        then it use the frequency.

        :param term: tag to parse
        :return: tag splitted in a list
        """
        if term.startswith('#'):
            term = term[1:]
        words = []
        # Remove hashtag, split by dash
        term = term.replace('-', ' ')
        term = term.replace('_', ' ')
        term = term.replace('+', ' ')
        term = term.replace('#', ' ')
        tags = re.sub(r"([0-9]+)", r" \1 ", term).split()
        for tag in tags:
            if len(tag) <= 2 or len(tag) > 50 or tag.isdigit():
                words.append(tag.lower())
            else:
                _, res = self.recursive_tokenizer(tag.lower())
                words.extend(res)
        return words

    def recursive_tokenizer(self, term):
        """
        This is the actual magic of the class ;)

        :param term: all low case tag to split
        :return: most probable bag of words
        """
        max_freq = self.freq(term)
        results = [term]
        for i in range(len(term), 0, -1):
            word = term[0:i]
            word_frequency = self.freq(word)
            if word_frequency > 0:
                s_frequency, rest = self.recursive_tokenizer(term[i:])
                word_frequency = word_frequency*s_frequency/2
                if word_frequency > max_freq:
                    max_freq = word_frequency
                    results = [word]
                    results.extend(rest)
        return max_freq, results

    def freq(self, word):
        """
        Return the frequency of a word.

        :param word: word to check
        :return: frequency (0 if not in dictionary)
        """
        if word not in self.__freqs__:
            return 0
        return self.__freqs__[word]

    def find_word(self, word):
        """
        Check if a word is the dictionary.

        :param word: word to check
        :return: boolean
        """
        return word in self.__freqs__


if __name__ == "__main__":
    def __test__(line):
        line = line.replace('\n', '')
        tag = line.split(',')[0]
        expected = line.split(',')[1:]
        done = ' '.join(SPLITTER.tokenize_tag(tag))
        output = tag+' -> '+done
        if done not in expected:
            output += ' \033[1;31m'+str(expected)+'\033[0m'
        else:
            output += ' \033[1;32m'+str(expected)+'\033[0m'
        print(output)
        return 1 if done in expected else 0
    PATH = 'resources/freqs.json'
    if len(sys.argv) == 2:
        PATH = sys.argv[1]

    SPLITTER = HashTagTokenizer(PATH)

    with open('resources/1000tags') as tags_file:
        LINES = tags_file.readlines()
    RESULT = 0
    TIME = time.time()
    for l in LINES:
        RESULT += __test__(l)
    TIME = time.time()-TIME
    print('Time: {}'.format(TIME))
    PERC = float(RESULT)/len(LINES)*100
    print('Total: {}/{} \033[1;32m({} %)\033[0m'.format(RESULT,
                                                        len(LINES),
                                                        PERC))
