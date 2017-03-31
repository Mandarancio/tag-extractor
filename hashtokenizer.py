#! /usr/bin/python3
# Martino Ferrari
import re
import time
import json


class SimpleTokenizer:
    def parse_tag(self, term):
        '''
        Simple Splitter based on capitals, dash and underscores.
        @Martino Ferrari
        :param term: tag to split
        :return: array of splitted words
        '''
        words = []
        # Remove hashtag, split by dash
        term = term.replace('-', ' ').replace('_', ' ').replace('+', ' ')
        tags = re.sub(r"([A-Z])", r" \1", term).split()
        return tags


class HashTagTokenizer:
    '''
    High-perforamnce Advanced hashtag tokenizerr using frequency of possible word
    combination to split correctly the tag.
    @Martino Ferrari
    :param freq_file: json frequency wordlist
    '''
    def __init__(self, freq_file):
        fp = open(freq_file)
        self.__freqs__ = json.load(fp)
        fp.close()

    def tokenize_tag(self, term):
        '''
        parse a tag, first step use standarad delimiter, numbers to split
        then it use the frequency
        :param term: tag to parse
        :return: tag splitted in a list
        '''
        if term.startswith('#'):
            term = term[1:]
        words = []
        # Remove hashtag, split by dash
        term = term.replace('-', ' ').replace('_', ' ').replace('+', ' ')
        tags = re.sub(r"([0-9]+)", r" \1 ", term).split()
        for tag in tags:
            if len(tag) <= 2 or len(tag) > 50 or tag.isdigit():
                words.append(tag.lower())
            else:
                _, res = self.recursive_tokenizer(tag.lower())
                words.extend(res)
        return words

    def recursive_tokenizer(self, term):
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
                fr, rest = self.recursive_tokenizer(term[i:])
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
    import sys
    def test(line):
        line = line.replace('\n', '')
        tag = line.split(',')[0]
        expected = line.split(',')[1:]
        done = ' '.join(splitter.tokenize_tag(tag))
        output = tag+' -> '+done
        if done not in expected:
            output += ' \033[1;31m'+str(expected)+'\033[0m'
        else:
            output += ' \033[1;32m'+str(expected)+'\033[0m'
        print(output)
        return 1 if done in expected else 0
    path = 'resources/freqs.json'
    if len(sys.argv) == 2:
       path = sys.argv[1]

    splitter = HashTagTokenizer(path)

    fp = open('resources/1000tags')
    lines = fp.readlines()
    fp.close()
    res = 0
    t = time.time()
    for l in lines:
        res += test(l)
    t = time.time()-t
    print('Time: '+str(t))
    print('Total: '+str(res)+'/'+str(len(lines))+' \033[1;32m(' +
          str(float(res)/len(lines)*100)+'%)\033[0m')
