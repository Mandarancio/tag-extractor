#! /usr/bin/python3
"""Frequency extraction utilities.

author: Martino Ferrari
"""
from nltk import FreqDist
from nltk.corpus import webtext
from nltk.corpus import brown


def to_dic(freqs, factor=1):
    """Transform NLTK frequency list to dictionary."""
    res = {}
    tot = 0
    for freq in freqs:
        if len(freq[0]) > 1:
            res[freq[0]] = freq[1]
            tot += freq[1]
        elif freq[0] == 'a' or freq[0] == 'i':
            res[freq[0]] = freq[1]
            tot += freq[1]
    for k in res:
        res[k] /= factor*tot
    return res


if __name__ == "__main__":
    import sys
    import json
    if len(sys.argv) != 2:
        print("\nUsage:\n  freqextractor OUTPUTFILE")
        sys.exit(0)
    PATH = sys.argv[1]
    MOST_100000 = {}
    FREQUENCY_LIST = FreqDist(i.lower() for i in webtext.words())
    MOST_100000.update(to_dic(FREQUENCY_LIST.most_common(100000), 2))
    FREQUENCY_LIST = FreqDist(i.lower() for i in brown.words())
    MOST_100000.update(to_dic(FREQUENCY_LIST.most_common(100000)))
#    most_100000['iphone'] = 5e-5
#    most_100000['ipad'] = 5e-5
    MOST_100000['smartphone'] = 5e-5
    MOST_100000['blog'] = 1e-5
    MOST_100000['blogger'] = 0.5e-5
    MOST_100000['bloggers'] = 0.5e-5
    MOST_100000['youtube'] = 0.5e-5
    MOST_100000['youtubber'] = 0.1e-5
    MOST_100000['youtubbers'] = 0.1e-5
    MOST_100000['vlogger'] = 0.2e-5
    MOST_100000['vloggers'] = 0.2e-5
    MOST_100000['instagram'] = 0.5e-5
    MOST_100000['instagramer'] = 0.5e-5
    MOST_100000['instagramers'] = 0.5e-5
    MOST_100000['instagrammer'] = 0.5e-5
    MOST_100000['instagrammers'] = 0.5e-5
    MOST_100000['twitter'] = 0.5e-5
    MOST_100000['porn'] = 1e-5
    MOST_100000['pic'] = 1e-5
    MOST_100000['pict'] = 1e-5
    MOST_100000['iger'] = 1e-5
    MOST_100000['igers'] = 1e-5
    MOST_100000['twit'] = 0.7e-5
    MOST_100000['insta'] = 2e-5
    MOST_100000['linux'] = 0.1e-6
    MOST_100000['ig'] = 0.1e-5
    with open(PATH, 'w') as json_file:
        json.dump(MOST_100000, json_file)
