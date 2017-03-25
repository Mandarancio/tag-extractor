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
## Pipeline
To be able to get overall good performance of the project its important to use a yield Pipeline.
In this way the API calls are not blocking, try the example to understand better.
A good example of it can be found at https://brett.is/writing/about/generator-pipelines-in-python/
