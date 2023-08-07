import requests


class APIRequest:
    def send_get_request(self, url):
        response = requests.get(url)
        return response.json()

    def send_post_request(self, url, data):
        response = requests.post(url, json=data)
        return response.json()
