#! /usr/bin/python3
import extractors as exs


def prettifier(photos):
    '''
    simple function to explain the use of a Pipeline
    :photos: list of extracted photos
    :return: list of pretty strings
    '''
    for photo in photos:
        if len(photo['tags']) > 0:
            string = ' + '+photo['id']+' ['+photo['lat']+
            ', '+photo['lon']+']:\n'
            for tag in photo['tags']:
                string += '\t- '+tag['tag']+'\n'

            yield string
        else:
            yield ' - '+photo['id']+' ['+photo['lat']+', '+photo['lon']+']'


if __name__ == '__main__':
    # please do not publish it on github
    apikey = u'YOUR_API_KEY'
    secret = u'YOUR_SECRET_KEY'

    f = exs.FlickrExtractor(apikey, secret)
    pipeline = prettifier(f.get_tags(lat=46.205850, lon=6.157521,
                                     radius=1, num_photos=50))
    for pretty in pipeline:
        print(pretty)
