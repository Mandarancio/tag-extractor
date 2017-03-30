import extractors as exs
import hashstokenizer
print('loading demo....')
demoExt = exs.JsonExtractor('demophotos.json')
print('loading splitter....')
splitter = hashtokenizer.HashTagTokenizer('freqs.json')
print('splitting....')
for p in demoExt.get_tags(0, 0, 1, -1):
    for t in p['tags']:
        splitted = ' '.join(splitter.tokenize_tag(t['raw']))
        print(t['raw']+' -> '+splitted)
