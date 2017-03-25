# tag-extractor
Python Flickr and Instagram tag extractor (by location) using python3

## Requirements

For Flickr use the library [flickrapi](https://stuvel.eu/flickrapi-doc/):
```bash
pip3 install flickrapi
# or eventually
python3-pip install flickrapi
```

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
  'posted': '1100897479',
  'taken': '2004-11-19 12:51:19',
  'tags': [
    {
      'id': '128760875-32795752924-60504812',
      'tag': 'instagramapp',
      'raw': 'instagram app'
    },
    {
      'id': '128760875-32795752924-1628',
      'tag': 'square',
      'raw': 'square'
    },
    {
      'id': '128760875-32795752924-110794',
      'tag': 'aden',
      'raw': 'Aden'
    }
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
