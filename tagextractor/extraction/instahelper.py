#! /usr/bin/python3
"""Instagram information extraction module.

author: Martino Ferraari
"""
import requests as r


def get_info_from_url(url):
    '''
    Recover basic info of an instagram photo from its URL
    :param url: url of the instagram post
    :return: dictionary contains basic informations and hashtags
    '''
    request = "https://api.instagram.com/oembed/?url="+url
    res = r.get(request)
    if res.text == "No Media Match":
        return {
            'media_id': None,
            'author_id': None,
            'tags': []
        }

    if res.status_code == 200:
        res = res.json()
        media_id = res['media_id']
        author_id = res['author_id']
        text = res['title'].split(' ')
        tags = []
        for word in text:
            if word.startswith('#'):
                tags.append(word)
        return {
            'media_id': media_id,
            'author_id': author_id,
            'image_url': res['thumbnail_url'],
            'tags': tags
        }
    return {
        'media_id': '',
        'author_id': '',
        'image_url': '',
        'tags': []
    }
