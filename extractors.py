#! /usr/bin/python3
# Martino Ferrari
import flickrapi
import twitthelper
import instahelper
import math
import json


class Extractor:
    def __init__(self, name):
        self.__name__ = name

    def name(self):
        return self.__name__

    def n_photos(self, lat, lon, radius):
        '''
        Method to retrive the number of photos in a certain region
        :param lat: latitude
        :param lon: longitude
        :param radius: radius in km (max 32)
        :return: the number of photos avaible
        '''
        return 0

    def get_tags(self, lat, lon, radius, num_photos=-1):
        '''
        Method to retrive the list of photos with teirs tags and position
        :param lat: latitude
        :param lon: longitude
        :param radius: radius in km (max 32)
        :param num_photos: number of photos to retrive (if -1: all avaible)
        :return: the list of photos with teirs tags and position (using yield)
        '''
        yield {}


class JsonExtractor(Extractor):
    '''
    Simple demo extractor, take data from json file
    @Martino Ferrari
    '''
    def __init__(self, file_path):
        Extractor.__init__(self, 'Json')
        self.__file_path__ = file_path
        f = open(file_path)
        self.__data__ = json.load(f)
        f.close()

    def n_photos(self, lat, lon, radius):
        return len(self.__data__['photos'])

    def get_tags(self, lat, lon, radius=1, num_photos=-1):
        if num_photos == -1 or num_photos >= self.n_photos(lat, lon, radius):
            num_photos = self.n_photos(lat, lon, radius)
        for i in range(0, num_photos):
            yield self.__data__['photos'][i]


class TwitInstaExtractor(Extractor):
    '''
    Simple instagram photo tags extractor by twitted photo location
    @Martino Ferrari
    '''
    def __init__(self, tw_access_key, tw_access_secret, tw_consumer_key,
                 tw_consumer_secret):
        Extractor.__init__(self, 'TwitInsta')
        self.__twith__ = twitthelper.TwittHelper(tw_access_key,
                                                 tw_access_secret,
                                                 tw_consumer_key,
                                                 tw_consumer_secret)

    def n_photos(self, lat, lon, radius):
        # TODO implement a method to retrive the number of twit ijn area
        # and avarage it to know the aproximative number of photos
        return -1

    def get_tags(self, lat, lon, radius=1, num_photos=-1):
        # TODO implement n_photos function
        if num_photos < 0:
            raise NameError('retrive all photos not yet implemented, \
                            please specify the number of pictures')
        for twit in \
            self.__twith__.get_twits_with_instagram_by_location(lat, lon,
                                                                radius,
                                                                num_photos):
            pobj = {}
            pobj['id'] = twit['instainfo']['media_id']
            pobj['owner'] = twit['instainfo']['author_id']
            pobj['tags'] = []
            for tag in twit['instainfo']['tags']:
                pobj['tags'].append({
                    'id': tag,
                    'raw': tag[1:],
                    'tag': tag[1:]
                })
            pobj['posted'] = twit['created_at']
            pobj['taken'] = twit['created_at']
            pobj['lat'] = twit['lat']
            pobj['lon'] = twit['lon']
            pobj['ntags'] = len(twit['instainfo']['tags'])
            yield pobj


class FlickrExtractor(Extractor):
    '''
    Simple flickr photo tags extractor by location
    @Martino Ferrari
    '''
    def __init__(self, apikey, secret):
        Extractor.__init__(self, 'Flickr')
        self.__apikey__ = apikey
        self.__secret__ = secret
        self.__flickr__ = flickrapi.FlickrAPI(apikey, secret)

    def n_photos(self, lat, lon, radius):
        rsp = self.__flickr__.photos.search(lat=lat, lon=lon, radius=radius,
                                            radius_units="km", per_page=100)
        if rsp.get('stat') == 'ok':
            return int(rsp.find('photos').get('total'))
        else:
            return 0

    def get_tags(self, lat, lon, radius, num_photos=-1):
        if num_photos == -1:
            num_photos = self.n_photos(lat, lon, radius)
        pages = math.ceil(num_photos/250.)
        per_page = 250
        if pages == 1 and num_photos < per_page:
            per_page = num_photos
        count = 0
        for p in range(1, pages+1):
            for photo in self.__get_tags__(lat, lon, radius, page=p,
                                           per_page=per_page):
                yield photo
                count += 1
                if count >= num_photos:
                    break

    def __get_tags__(self, lat, lon, radius, page=1, per_page=100):
        page = self.__flickr__.photos.search(lat=lat, lon=lon, radius=radius,
                                             radius_units="km",
                                             per_page=per_page, page=page)
        if page.get('stat') == 'ok':
            for photo in page.iter('photo'):
                pobj = {}
                pobj['id'] = photo.get('id')
                pobj['owner'] = photo.get('owner')
                pobj['tags'] = []
                info = self.__flickr__.photos.getInfo(photo_id=pobj['id'])
                pinfo = info.find('photo')
                tags = pinfo.find('tags')
                for tag in tags.iter('tag'):
                    pobj['tags'].append({
                        'id': tag.get('id'),
                        'raw': tag.get('raw'),
                        'tag': tag.text
                    })
                date = pinfo.find('dates')
                pobj['posted'] = date.get('posted')
                pobj['taken'] = date.get('taken')
                pobj['ntags'] = len(pobj['tags'])
                if len(pobj['tags']) > 0:
                    geoloc = self.__flickr__.photos.geo.getLocation(
                        photo_id=pobj['id'])
                    loc = geoloc.find('photo').find('location')
                    pobj['lat'] = loc.get('latitude')
                    pobj['lon'] = loc.get('longitude')
                else:
                    # if there are no tags there is no need to have the exact
                    # position
                    pobj['lat'] = str(lat)
                    pobj['lon'] = str(lon)
                yield pobj
        else:
            yield {}
