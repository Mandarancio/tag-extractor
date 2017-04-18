# tag-extractor
Python *Flickr* and *Instagram* tag extractor (by location) using **Python 3**

## Dependencies

The project uses multiple standard python libraries:
 - [nltk](http://www.nltk.org/howto/wordnet.html) (and the modules ```omw``` and ```brown```)
 - [unidecode](https://pypi.python.org/pypi/Unidecode)
 - [SQLAlchemy](http://docs.sqlalchemy.org/en/latest/)
 - [flickrapi](https://stuvel.eu/flickrapi-doc/)
 - [twitter](https://pypi.python.org/pypi/twitter)
 - [requests](http://docs.python-requests.org/en/master/)

To install this dependencies:
```bash
pip3 install nltk
pip3 install unidecode
pip3 install flickrapi
pip3 install twitter
pip3 install requests
```

To install the nltk modules, run the following ```python3``` script:
```python
#! /usr/bin/python3
import nltk
nltk.download("omw")
nltk.download("brown")
```

## Extraction Examples

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

## Data Structure

The photo and its tags are represented as a dictionary in this form

```python
{
  'id': '32795752924',
  'posted': '1100897479',
  'taken': '2004-11-19 12:51:19',
  'url' : 'https://www.flickr.com/photos/49625814@N05/34114294175',
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
  'ntags': 3,
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


## References and Links

### References
 - [A methodology for mapping Instagram hashtags](http://firstmonday.org/article/view/5563/4195)

### Links

 - [PyBabelfy](https://github.com/aghie/pybabelfy)
 - [python twitter examples](https://github.com/ideoforms/python-twitter-examples)
 - [Piplines in Python](https://brett.is/writing/about/generator-pipelines-in-python/)
 - [FlickrAPI bug fix](https://github.com/sybrenstuvel/flickrapi/issues/75)
