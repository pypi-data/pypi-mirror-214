
from functools import cached_property
from oneapi.api_resources.abstract.listable_api_resource import ListableAPIResource
from oneapi.api_resources.abstract.retrievable_api_resource import RetrievableAPIResource


class Movie(
    ListableAPIResource,
    RetrievableAPIResource,
):
    url_suffix = "movie"

    def __init__(self, _id: str, name: str, runtimeInMinutes: int, budgetInMillions: int, boxOfficeRevenueInMillions: int, academyAwardNominations: int, academyAwardWins: int, rottenTomatoesScore: int):
        self._id = _id
        self.name = name
        self.runtimeInMinutes = runtimeInMinutes
        self.budgetInMillions = budgetInMillions
        self.boxOfficeRevenueInMillions = boxOfficeRevenueInMillions
        self.academyAwardNominations = academyAwardNominations
        self.academyAwardWins = academyAwardWins
        self.rottenTomatoesScore = rottenTomatoesScore

    @cached_property
    def quotes(self):
        from oneapi.api_resources.quote import Quote

        return Quote.list(filter={"movie": ("=", self._id)})

    def __repr__(self):
        return f"<Movie id={self._id} name={self.name}>"