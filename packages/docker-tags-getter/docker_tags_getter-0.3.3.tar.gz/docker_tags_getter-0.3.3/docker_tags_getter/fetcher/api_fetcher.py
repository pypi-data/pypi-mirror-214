import requests

class ApiFetcher:
    """The handler of response."""
    def __init__(self, config):
        self.config = config

    def get(self, url) -> (int, dict|None):
        headers = self.config.get_headers()
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return (response.status_code, None)
        return (response.status_code, response.json())
