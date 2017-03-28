import requests as r


def get_info_from_url(url):
    request = "https://api.instagram.com/oembed/?url="+url
    res = r.get(request)
    if res.text == "No Media Match":
        return {
            'media_id': None,
            'author_id': None,
            'tags': []
        }
    res = res.json()
    media_id = res['media_id']
    author_id = res['author_id']
    text = res['title'].split(' ')
    tags = []
    for t in text:
        if t.startswith('#'):
            tags.append(t)
    return {
        'media_id': media_id,
        'author_id': author_id,
        'tags': tags
    }
