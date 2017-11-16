import requests


class GiphyApi:

    def __init__(self, key):
        self.api_key = key

    def get_random_gif(self, tag):
        r = requests.get('https://api.giphy.com/v1/gifs/random?api_key={}&tag={}&rating=R'.format(self.api_key, tag))
        try:
            response = r.json()
            return response['data']['url']
        except (RuntimeError, TypeError, NameError, ValueError, KeyError):
            return ''
