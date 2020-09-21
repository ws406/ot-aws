import requests
from src.utils.logger import OtLogger

# Build this request to fake genuine browser request.
class BrowserRequests:
    def __int__(self):
        pass

    @staticmethod
    def get(url, logger: OtLogger):
        logger.log('Handling URL - ' +  url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            raise requests.HTTPError

        return response
