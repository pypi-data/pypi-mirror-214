"""Simple SDK for exploring the the movie and quotes endpoints for the-one-api.dev."""

import requests
import pydantic
import os


class Movie(pydantic.BaseModel):
    """A LotR movie title."""

    id: str = pydantic.Field(None, alias="_id")
    name: str
    runtimeInMinutes: int
    budgetInMillions: int
    boxOfficeRevenueInMillions: int
    academyAwardNominations: int
    academyAwardWins: int
    rottenTomatoesScore: int


class Quote(pydantic.BaseModel):
    """A quote from LotR."""

    _id: str
    dialog: str
    movie: str
    character: str
    id: str


class LOTR:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("API_KEY")
        if not self.api_key:
            raise ValueError(
                "First arg must be api_key or must define API_KEY env variable"
            )

    def movies(self, id: str | None = None, limit=10, offset=0) -> list[Movie]:
        """List of all movies, including the "The Lord of the Rings" and the "The Hobbit" trilogies"""
        url = "movie"
        if id:
            url += "/" + id
        json_resp = self._get(url, limit, offset)
        return [Movie(**doc) for doc in json_resp["docs"]]

    def movie_quotes(self, id: str, limit=10, offset=0) -> list[Quote]:
        """Request all movie quotes for one specific movie (only working for the LotR trilogy)"""
        url = f"movie/{id}/quote"
        json_resp = self._get(url, limit, offset)
        return [Quote(**doc) for doc in json_resp["docs"]]

    def quotes(self, id: str | None = None, limit=10, offset=0) -> list[Quote]:
        """List of all movie quotes."""
        url = "quote"
        if id:
            url += "/" + id
        json_resp = self._get(url, limit, offset)
        return [Quote(**doc) for doc in json_resp["docs"]]

    def _get(self, endpoint, limit: int, offset: int):
        """Helper for querying api."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"limit": limit, "offset": offset}
        url = f"https://the-one-api.dev/v2/{endpoint}"
        resp = requests.get(url, params=params, headers=headers)
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    # Basic endpoints:
    # /movie
    # /movie/{id}
    # /movie/{id}/{quote}
    # /quote
    # /quote/{id}

    # Movie basics.
    lotr = LOTR()
    movies = lotr.movies(limit=5)
    assert len(movies) == 5
    movie_3 = movies[3]
    assert lotr.movies(id=movie_3.id)[0] == movie_3

    # Quote basics.
    quotes = lotr.quotes(limit=7)
    assert len(quotes) == 7
    quote_6 = quotes[6]
    assert lotr.quotes(id=quote_6.id)[0] == quote_6

    # Movie quotes (only works on original 3).
    all_movies = lotr.movies()
    two_towers = next(m for m in all_movies if m.name == "The Two Towers")
    movie_quotes = lotr.movie_quotes(id=two_towers.id, limit=11)
    assert len(movie_quotes) == 11
    assert all(isinstance(q, Quote) for q in movie_quotes)
