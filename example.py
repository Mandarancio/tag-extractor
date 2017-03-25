import extractors as exs

# please do not publish it on github
apikey = u'YOUR_API_KEY'
secret = u'YOUR_SECRET_KEY'

f = exs.FlickrExtractor(apikey, secret)

for photo in f.get_tags(lat=46.205850, lon=6.157521, radius=1, num_photos=25):
    if len(photo['tags']) > 0:
        print(photo)
    else:
        print('-')
