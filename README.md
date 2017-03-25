# tag-extractor
Python Flickr and Instagram tag extractor (by location)

## Usage

```python
import extractors as exs

apikey = u'YOUR_API_KEY'
secret = u'YOUR_SECRET_KEY'

f = exs.FlickrExtractor(apikey, secret)

for photo in f.get_tags(lat=46.205850, lon=6.157521, radius=1, num_photos=25):
    if len(photo['tags']) > 0:
        print(photo)
    else:
        print('-')
```
The output for a picture is a dictionary:
```python
{
  'id': '32795752924',
  'tags': [
    {'id': '128760875-32795752924-60504812', 'tag': 'instagramapp', 'raw': 'instagram app'},
    {'id': '128760875-32795752924-1628', 'tag': 'square', 'raw': 'square'},
    {'id': '128760875-32795752924-14976', 'tag': 'squareformat', 'raw': 'square format'},
    {'id': '128760875-32795752924-34115330', 'tag': 'iphoneography', 'raw': 'iphoneography'},
    {'id': '128760875-32795752924-60643605', 'tag': 'uploaded:by=instagram', 'raw': 'uploaded:by=instagram'},
    {'id': '128760875-32795752924-110794', 'tag': 'aden', 'raw': 'Aden'}
  ],
  'owner': '128806197@N06',
  'lon': '6.150000', 
  'lat': '46.200000'
}
```
## Pipeline
To be able to get overall good performance of the project its important to use a yield Pipeline.
In this way the API calls are not blocking, try the example to understand better.
A good example of it can be found at https://brett.is/writing/about/generator-pipelines-in-python/
