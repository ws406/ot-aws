import requests

# Build this request to fake genuine browser request.
class BrowserRequests:
    def __int__(self):
        pass

    @staticmethod
    def get(url):
        print('Handling URL - ' +  url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            raise requests.HTTPError

        return response

if __name__ == '__main__':
    br = BrowserRequests()
    print(br.get('http://1x2d.win007.com/1584249.js').status_code)
