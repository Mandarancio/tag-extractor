import extractors as exs
import instasplitter
print('loading demo....')
demoExt = exs.JsonExtractor('demophotos.json')
print('loading splitter....')
splitter = instasplitter.HashtagSplitter()
print('splitting....')
for p in demoExt.get_tags(0, 0, 1, -1):
    for t in p['tags']:
        splitted = ' '.join(splitter.parse_tag(t['raw']))
        print(t['raw']+' -> '+splitted)
