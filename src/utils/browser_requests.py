import requests
from src.utils.logger import OtLogger

# Build this request to fake genuine browser request.
class BrowserRequests:
    def __int__(self):
        pass

    @staticmethod
    def get(url, logger: OtLogger):
        logger.log('Handling URL - ' +  url)
        params = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            raise requests.HTTPError

        return response
