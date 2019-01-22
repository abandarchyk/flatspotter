import requests


class Endpoint:

    base_url = ''

    def __init__(self, bid):
        self.base_url = 'https://api.telegram.org/bot' + bid + '/'

    def http_get(self, url: str, data: dict):
            print('HTTP GET: ' + self.base_url + url)
            print(data)
            response = requests.get(self.base_url + url, data)
            return response

    def http_post(self, url: str, message):
        print('HTTP POST: ' + self.base_url + url)
        print('Request body:\n' + str(message))
        response = requests.post(self.base_url + url, data=message)
        return response

