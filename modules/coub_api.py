import requests
import random


class CoubApi:

    def get_random_coub(self):
        r = requests.get('http://coub.com/api/v2/timeline/explore/random', {'per_page': 25})
        try:
            response = r.json()
            rand_item = random.choice(response['coubs'])
            return 'http://coub.com/view/' + rand_item['permalink']
        except (RuntimeError, TypeError, NameError, ValueError, KeyError):
            return ''
