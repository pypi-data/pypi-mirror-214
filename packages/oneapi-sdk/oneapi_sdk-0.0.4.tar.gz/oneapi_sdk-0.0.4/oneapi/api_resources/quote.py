
from oneapi.api_resources.abstract.listable_api_resource import ListableAPIResource
from oneapi.api_resources.abstract.retrievable_api_resource import RetrievableAPIResource


class Quote(
    ListableAPIResource,
    RetrievableAPIResource,
):
    url_suffix = "quote"

    def __init__(self, _id, id, dialog, movie, character):
        self._id = _id
        self.id = id
        self.dialog = dialog
        self.movie = movie
        self.character = character

    def __repr__(self):
        return f"<Quote id={self.id} dialog={self.dialog} movie={self.movie} character={self.character}>"