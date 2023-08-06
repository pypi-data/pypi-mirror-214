from typing import TypeVar
from oneapi.api_resources.abstract.api_resource import APIResource


T = TypeVar("T")

class RetrievableAPIResource(APIResource):
    @classmethod
    def get(cls: type[T], id: str) -> T:
        response = cls.request("GET", f"{cls.url_suffix}/{id}")
        return cls(**response["docs"][0])
