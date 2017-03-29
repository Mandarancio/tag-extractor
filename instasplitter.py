#! /usr/bin/python3
import re


# Returns a list of common english terms (words)
def InitializeWords(path):
    wordlist = path
    # A file containing common english words
    content = None
    with open(wordlist) as f:
        content = f.readlines()
    return [word.rstrip('\n') for word in content]


def ParseTag(term, wordlist):
    words = []
    # Remove hashtag, split by dash
    term = term.replace('-', ' ').replace('_', ' ').replace('+', ' ')
    tags = re.sub(r"([A-Z])", r" \1", term).split()
    for tag in tags:
        if len(tag) == 1:
            words.append(tag)
        for i in range(2, len(tag)):
            print(RecursiveParse(tag, wordlist))


def RecursiveParse(term, wordlist):
    if len(term) <= 2:
        return term
    res = {}
    for i in range(2, len(term)+1):
        # print(term[0:i])
        if FindWord(term[0:i], wordlist):
            if i < len(term):
                res[term[0:i]] = RecursiveParse(term[i:], wordlist)
            else:
                res[''] = term
    if len(res) == 0:
        return None
    return res


def FindWord(token, wordlist):
    return token in wordlist


if __name__ == "__main__":
    wordlist = InitializeWords("words.txt")
    print(ParseTag("awesome-dayofmylife", wordlist))
