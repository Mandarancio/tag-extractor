import flickrapi
import math


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


class FlickrExtractor(Extractor):
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

                tags = self.__flickr__.tags_getListPhoto(photo_id=pobj['id'])
                for tag in tags.iter('tag'):
                    pobj['tags'].append({
                        'id': tag.get('id'),
                        'raw': tag.get('raw'),
                        'tag': tag.text
                    })
                if len(pobj['tags']) > 0:
                    geoloc = self.__flickr__.photos.geo.getLocation(
                        photo_id=pobj['id'])
                    loc = geoloc.find('photo').find('location')
                    pobj['lat'] = loc.get('latitude')
                    pobj['lon'] = loc.get('longitude')
                else:
                    # if there are no tags there is no need to have the exact
                    # position
                    pobj['lat'] = lat
                    pobj['lon'] = lon
                yield pobj
        else:
            yield {}
