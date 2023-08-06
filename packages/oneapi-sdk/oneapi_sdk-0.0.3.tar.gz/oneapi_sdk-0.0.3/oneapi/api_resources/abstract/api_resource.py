from oneapi.api_requestor import APIRequestor


class APIResource(object):
    @staticmethod
    def request(method, url_suffix, params=None, headers=None):
        return APIRequestor().request(method, url_suffix, params, headers).json()