import requests

class ApiHandler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def send_get(self, endpoint: str):
        """ Helper method to send a GET request"""
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url)

    def send_post(self, endpoint: str, payload: dict):
        """ Helper method to send a POST request"""
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, json=payload)