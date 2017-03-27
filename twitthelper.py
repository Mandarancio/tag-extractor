#! /usr/bin/python3
import twitter


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
        query = self.__api__.search.tweets(q="",
                                           geocode="%f,%f,%dkm" % (lat, lon,
                                                                   radius),
                                           count=number_twits, max_id=None)
        for result in query["statuses"]:
            if result["geo"]:
                    user = result["user"]["screen_name"]
                    text = result["text"]
                    text = text.encode('ascii', 'replace')
                    latitude = result["geo"]["coordinates"][0]
                    longitude = result["geo"]["coordinates"][1]
                    row = {
                            'user': user,
                            'text': text,
                            'lat': latitude,
                            'lon': longitude
                          }
                    yield row
