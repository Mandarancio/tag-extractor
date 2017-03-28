# tag-extractor
Python *Flickr* and *Instagram* tag extractor (by location) using **Python 3**

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


## Instagram
A simple library to use *Instagram* is [python-instagram](https://github.com/facebookarchive/python-instagram):
```bash

pip3 install python-instagram
# or eventually
python3-pip install python-instagram

```

To use it, as is not yet implemented in the library, here some examples:

```python
from instagram.client import InstagramAPI

access_token = "YOUR_ACCESS_TOKEN"
client_secret = "CLIENT_SECRET"
api = InstagramAPI(access_token=access_token, client_secret=client_secret)

# retrive the list of instagram location in a radius of 100 meters
for loc in api.location_search(lat=46.205850, lng=6.157521):
    print(loc.name+' : '+loc.id)
    # retrive the last 10 photos of each location
    api.location_recent_media(location_id=loc.id,count=10)

```

(To get the access token follow the following tutorial: [link](https://bobmckay.com/web/simple-tutorial-for-getting-an-instagram-clientid-and-access-token))

However to be really able to have access to the data we need or the agreement of the users or the agreement of Instagram (trough a quite hard selection process). [READ HERE](https://www.instagram.com/developer/sandbox/)
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

## Where to test your code?

If you wish to test your code with personal apikey or trash code, please do it and name your script ```{FILE NAME}_test.py```, this will be automatically ignored by git (look at ```.gitignore``` file to understand why). 

## Links

https://github.com/aghie/pybabelfy
