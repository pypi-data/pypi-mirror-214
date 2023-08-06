from typing import Generic, List, TypeVar
from oneapi.api_resources.abstract.api_resource import APIResource
from oneapi.api_resources.utils import Sort, UrlQueryFromFilters

T = TypeVar("T")

class ListResponse(Generic[T]):
    def __init__(
        self,
        items: List[T],
        total,
        limit,
        offset,
        sort,
        filter,
        request_cls: "ListableAPIResource",
    ):
        self._items = items
        self._meta = {"total": total, "limit": limit, "offset": offset, "sort": sort, "filter": filter}
        self._request_cls = request_cls

    def __iter__(self):
        return self._items.__iter__()

    def __getitem__(self, index) -> T:
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def auto_paginate(self):
        for item in self._items:
            yield item
        offset = self._meta.get("offset", 0)
        limit = self._meta.get("limit", 10)
        total = self._meta.get("total", 0)
        if offset + limit < total:
            sort = self._meta.get("sort", None)
            filter = self._meta.get("filter", None)
            next_page = self._request_cls.list(
                limit=limit,
                offset=offset + limit,
                sort=sort,
                filter=filter,
            )
            yield from next_page.auto_paginate()


class ListableAPIResource(APIResource):
    @classmethod
    def list(
        cls: type[T], *, limit=10, offset=0, sort: str = None, filter: dict = None
    ) -> ListResponse[T]:
        if sort is not None:
            sort = Sort.parse(sort)
        if filter is not None:
            filter = UrlQueryFromFilters.parse(filter)

        params = {"limit": limit, "offset": offset, "sort": sort}
        url_suffix = f"{cls.url_suffix}?{filter}" if filter else cls.url_suffix
        json_response = cls.request("GET", url_suffix, params=params)
        items = [cls(**item) for item in json_response["docs"]]
        return ListResponse(
            items=items,
            total=json_response["total"],
            limit=limit,
            offset=offset,
            sort=sort,
            filter=filter,
            request_cls=cls,
        )
