from oneapi.api_resources.utils import Sort, UrlQueryFromFilters
import pytest


class TestUrlQueryFromFilters:
    def test_empty(self):
        assert UrlQueryFromFilters.parse({}) == ""

    def test_single(self):
        assert UrlQueryFromFilters.parse({"a": ("=", "b")}) == "a=b"

    def test_multiple(self):
        assert (
            UrlQueryFromFilters.parse({"a": ("=", "b"), "c": ("=", "d")}) == "a=b&c=d"
        )

    def test_exists(self):
        assert UrlQueryFromFilters.parse({"a": ("exists",)}) == "a"

    def test_not_exists(self):
        assert UrlQueryFromFilters.parse({"a": ("not_exists",)}) == "!a"

    def test_multiple_exists(self):
        assert UrlQueryFromFilters.parse({"a": ("exists",), "b": ("exists",)}) == "a&b"

    def test_multiple_not_exists(self):
        assert (
            UrlQueryFromFilters.parse({"a": ("not_exists",), "b": ("not_exists",)})
            == "!a&!b"
        )

    def test_all_possible_filters(self):
        assert (
            UrlQueryFromFilters.parse(
                {
                    "a": ("=", "b"),
                    "c": ("!=", "d"),
                    "e": ("<", "f"),
                    "g": (">", "h"),
                    "i": (">=", "j"),
                    "k": ("exists",),
                    "l": ("not_exists",),
                }
            )
            == "a=b&c!=d&e<f&g>h&i>=j&k&!l"
        )

    def test_invalid_operator(self):
        with pytest.raises(ValueError):
            UrlQueryFromFilters.parse({"a": ("invalid",)})


class TestSort:
    def test_asc(self):
        assert str(Sort.asc("a")) == "a:asc"

    def test_desc(self):
        assert str(Sort.desc("a")) == "a:desc"

    def test_parse_asc(self):
        assert str(Sort.parse("a")) == "a:asc"

    def test_parse_desc(self):
        assert str(Sort.parse("-a")) == "a:desc"
