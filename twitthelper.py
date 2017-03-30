#! /usr/bin/python3
# Martino Ferrari
import twitter
import instahelper


class TwittHelper:
    '''
    Simple class to help to retrive twits by location.
    @Martino Ferrari
    '''
    def __init__(self, access_key, access_secret, consumer_key,
                 consumer_secret):
        self.__api__ = twitter.Twitter(
            auth=twitter.OAuth(access_key,
                               access_secret,
                               consumer_key,
                               consumer_secret))

    def get_twits_by_location(self, lat, lon, radius=1, number_twits=100):
        '''
        Retrive last twits by location
        :param lat: latitude
        :param lon: longitude
        :param radius: radius in km
        :param number_twits: number of twits to reterive (default 100)
        :return: yield with twits, user and location
        '''

        last_id = None
        result_count = 0
        while result_count < number_twits:
            query = self.__api__.search.tweets(q="",
                                               geocode="%f,%f,%dkm" % (lat,
                                                                       lon,
                                                                       radius),
                                               count=100, max_id=last_id)
            for result in query["statuses"]:
                if result["geo"]:
                    print(result["entities"]["urls"][0])
                    user = result["user"]["screen_name"]
                    text = result["text"]
                    created_at = result["created_at"]
                    text = text.encode('ascii', 'replace')
                    latitude = result["geo"]["coordinates"][0]
                    longitude = result["geo"]["coordinates"][1]
                    row = {
                            'user': str(user),
                            'text': text,
                            'lat': str(latitude),
                            'lon': str(longitude),
                            'url': None,
                            'lang': result['lang'],
                            'created_at': created_at,
                            'instainfo': None
                          }
                    result_count += 1
                    yield row
                last_id = result["id"]

    def get_twits_with_instagram_by_location(self, lat, lon, radius=1,
                                             number_twits=100):
        '''
        Retrive last twits by location that contains a link to instagram
        :param lat: latitude
        :param lon: longitude
        :param radius: radius in km
        :param number_twits: number of twits to reterive (default 100)
        :return: yield with twits, user, location, url and instagram photo id
        '''

        last_id = None
        result_count = 0
        while result_count < number_twits:
            query = self.__api__.search.tweets(q="",
                                               geocode="%f,%f,%dkm" % (lat,
                                                                       lon,
                                                                       radius),
                                               count=100, max_id=last_id)
            for result in query["statuses"]:
                if result["geo"]:
                    if len(result["entities"]["urls"]) == 1 and \
                            'www.instagram.com' in \
                            result["entities"]["urls"][0]["expanded_url"]:
                        created_at = result["created_at"]
                        user = result["user"]["screen_name"]
                        text = result["text"]
                        text = text.encode('ascii', 'replace')
                        latitude = result["geo"]["coordinates"][0]
                        longitude = result["geo"]["coordinates"][1]

                        url = result["entities"]["urls"][0]["expanded_url"]
                        instaid = url.split('/')[-2]
                        info = instahelper.get_info_from_url(url)
                        if info['media_id'] is not None:
                            row = {
                                    'user': str(user),
                                    'text': text,
                                    'lat': str(latitude),
                                    'lon': str(longitude),
                                    'url': str(url),
                                    'lang': result['lang'],
                                    'created_at': created_at,
                                    'instainfo': info
                                  }
                            result_count += 1
                            yield row
                    last_id = result['id']
