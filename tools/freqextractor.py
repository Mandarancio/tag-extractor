#! /usr/bin/python3
# Martino Ferrari
from nltk import FreqDist
from nltk.corpus import brown


def to_dic(freqs):
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


if __name__ == "__main__":
    import sys
    import json
    if len(sys.argv) != 2:
        print("\nUsage:\n  freqextractor OUTPUTFILE")
        sys.exit(0)
    path = sys.argv[1]

    frequency_list = FreqDist(i.lower() for i in brown.words())
    fp = open(path, 'w')
    most_100000 = to_dic(frequency_list.most_common(100000))
    most_100000['iphone'] = 5e-5
    most_100000['smartphone'] = 5e-5
    most_100000['blog'] = 1e-5
    most_100000['blogger'] = 0.5e-5
    most_100000['youtube'] = 0.5e-5
    most_100000['youtubber'] = 0.1e-5
    most_100000['vlogger'] = 0.2e-5
    most_100000['instagram'] = 0.5e-5
    most_100000['twitter'] = 0.5e-5
    most_100000['porn'] = 1e-5
    most_100000['pic'] = 1e-5
    most_100000['repost'] = 0.7e-5
    most_100000['twit'] = 0.7e-5
    most_100000['insta'] = 0.1e-6
    most_100000['linux'] = 0.1e-6
    json.dump(most_100000, fp)
    fp.close()
