import requests


class APIRequestor(object):
    def __init__(self) -> None:
        import oneapi

        self.access_token = oneapi.access_token
        self.base_url = "https://the-one-api.dev/v2/"

    def request(self, method, url_suffix, params=None, headers=None):
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        url = self.base_url + url_suffix
        headers["Authorization"] = "Bearer " + self.access_token
        response = requests.request(method, url, params=params, headers=headers)
        self._handle_api_error(response)
        return response

    def _handle_api_error(self, response: requests.Response):
        if not response.ok:
            response.raise_for_status()