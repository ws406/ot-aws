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
            "content-type":"text"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise requests.HTTPError

        return response
