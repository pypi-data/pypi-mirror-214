from unittest.mock import patch
import oneapi
from oneapi.tests.mocks import MOVIES, QUOTES, create_response


class TestMovies:
    @patch(
        "oneapi.api_resources.abstract.api_resource.APIResource.request",
        return_value=create_response(MOVIES),
    )
    def test_list_movies(self, mock_request):
        oneapi.access_token = "test"
        movies = oneapi.Movie.list()
        assert len(movies) == 3

    @patch(
        "oneapi.api_resources.abstract.api_resource.APIResource.request",
        return_value=create_response([MOVIES[0]]),
    )
    def test_get_movie(self, mock_request):
        oneapi.access_token = "test"
        movie = oneapi.Movie.get("5cd95395de30eff6ebccde5c")
        assert movie._id == "5cd95395de30eff6ebccde5c"

    @patch(
        "oneapi.api_resources.abstract.api_resource.APIResource.request",
        side_effect=[
            create_response(MOVIES[:1], 3),
            create_response(MOVIES[1:2], 3),
            create_response(MOVIES[2:], 3),
        ],
    )
    def test_list_autopaginate(self, mock_request):
        oneapi.access_token = "test"
        movies = oneapi.Movie.list(limit=1, offset=0)
        assert len(movies) == 1
        assert movies._meta["total"] == 3
        for movie in movies.auto_paginate():
            assert movie._id in [m["_id"] for m in MOVIES]

        assert mock_request.call_count == 3

    @patch(
        "oneapi.api_resources.abstract.api_resource.APIResource.request",
        side_effect=[create_response([MOVIES[0]]), create_response(QUOTES)],
    )
    def test_movie_quotes(self, mock_request):
        oneapi.access_token = "test"
        movie = oneapi.Movie.get("5cd95395de30eff6ebccde5c")
        assert movie._id == "5cd95395de30eff6ebccde5c"
        quotes = movie.quotes
        assert len(quotes) == 3
        assert mock_request.call_count == 2


class TestQuotes:
    @patch(
        "oneapi.api_resources.abstract.api_resource.APIResource.request",
        return_value=create_response(QUOTES),
    )
    def test_list_quotes(self, mock_request):
        oneapi.access_token = "test"
        quotes = oneapi.Quote.list()
        assert len(quotes) == 3

    @patch(
        "oneapi.api_resources.abstract.api_resource.APIResource.request",
        return_value=create_response([QUOTES[0]]),
    )
    def test_get_quote(self, mock_request):
        oneapi.access_token = "test"
        quote = oneapi.Quote.get("5cd95395de30eff6ebccde5f")
        assert quote._id == "5cd95395de30eff6ebccde5f"

    @patch(
        "oneapi.api_resources.abstract.api_resource.APIResource.request",
        side_effect=[
            create_response(QUOTES[:1], 3),
            create_response(QUOTES[1:2], 3),
            create_response(QUOTES[2:], 3),
        ],
    )
    def test_list_autopaginate(self, mock_request):
        oneapi.access_token = "test"
        quotes = oneapi.Quote.list(limit=1, offset=0)
        assert len(quotes) == 1
        assert quotes._meta["total"] == 3
        for movie in quotes.auto_paginate():
            assert movie._id in [m["_id"] for m in QUOTES]

        assert mock_request.call_count == 3
