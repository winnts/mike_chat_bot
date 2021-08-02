import requests
import json
import random


def get_public_feed():
    response = requests.request("GET", "https://api.flickr.com/services/feeds/photos_public.gne?format=json").text
    dump_response = response.removeprefix("jsonFlickrFeed(").removesuffix(")")
    return json.loads(dump_response)


def get_random():
    images = []
    for item in get_public_feed()['items']:
        images.append({'link': item['media']['m'], 'title': item['title']})
    return random.choice(images)


# print(get_random())
