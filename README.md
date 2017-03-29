# tag-extractor
Python *Flickr* and *Instagram* tag extractor (by location) using **Python 3**


## NLTK

For *NLTK* use the library [nltk]:
```bash

pip3 install nltk
# or eventually
python3-pip install nltk

```


## Flicrk

For *Flickr* use the library [flickrapi](https://stuvel.eu/flickrapi-doc/):
```bash

pip3 install flickrapi
# or eventually
python3-pip install flickrapi

```

An api key is required (I have one for our projects)
## Twitter
A simple library is the official [twitter](https://pypi.python.org/pypi/twitter):
```bash

pip3 install twitter
# or eventually
python3-pip install twitter

```

  A simple helper to retrieve twits by location is ```twitthelper.py```, look inside it to understand better ;).


## Instagram and Twitter

To use the simple extractor for instagram based on twits you need the following libraries:
```bash

pip3 install requests
pip3 install twitter

```

Than you will need the apikey and access code of twitter (very easy to get, please look at twetter developer documents).

### References
[A methodology for mapping Instagram hashtags](http://firstmonday.org/article/view/5563/4195)

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

With instagram:

```python
import extractors as exs

twitInstExt =exs.TwitInstaExtractor(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY,
                       CONSUMER_SECRET)

for photo in twitInstExt.get_tags(lat=46.205850, lon=6.157521, radius=1,
                                  num_photos=25):
    print(photo)
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
      'raw': 'instagram app',
      'lemmas': [],
      'hypernyms':[]
    },
    {
      'id': '128760875-32795752924-1628',
      'tag': 'square',
      'raw': 'square',
      'lemmas':['square', 'foursquare', 'second_power'],
      'hypernyms':['rectangle.n.01', 'regular_polygon.n.01', 'number.n.02']
    },
    {
      'id': '128760875-32795752924-110794',
      'tag': 'aden',
      'raw': 'Aden',
      'lemmas':['Aden'],
      'hypernyms':[]
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

## Where to test your code?

If you wish to test your code with personal apikey or trash code, please do it and name your script ```{FILE NAME}_test.py```, this will be automatically ignored by git (look at ```.gitignore``` file to understand why).

## Links

https://github.com/aghie/pybabelfy
