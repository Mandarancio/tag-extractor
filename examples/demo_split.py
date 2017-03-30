import extractors as exs
import hashsplitter
print('loading demo....')
demoExt = exs.JsonExtractor('demophotos.json')
print('loading splitter....')
splitter = instasplitter.HashtagSplitter('freqs.json')
print('splitting....')
for p in demoExt.get_tags(0, 0, 1, -1):
    for t in p['tags']:
        splitted = ' '.join(splitter.parse_tag(t['raw']))
        print(t['raw']+' -> '+splitted)
