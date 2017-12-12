# from urllib.request import urlopen
import urllib3
from bs4 import BeautifulSoup

class GamesFetcher:

    url_games_list = ''

    def __init__(self):
        pass

    def get_next_games(self):
        http = urllib3.PoolManager()
        response = http.request('GET', )

        return response.data
        pass
