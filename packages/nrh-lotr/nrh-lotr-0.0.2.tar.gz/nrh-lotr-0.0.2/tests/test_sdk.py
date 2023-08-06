"""NOTE: These tests assume the user has a environment variable named API_KEY
with a valid api key from the-one-api.
More here: https://the-one-api.dev/documentation#3

Define like: `export API_KEY=SOME_API_KEY`

TODO: can probably mock that layer using something like: https://pypi.org/project/httmock/
"""

from lotr import LOTR, Movie, Quote


def test_movie():
    # Movie basics.
    lotr = LOTR()
    movies = lotr.movies(limit=5)
    assert len(movies) == 5
    movie_3 = movies[3]
    assert lotr.movies(id=movie_3.id)[0] == movie_3


def test_quotes():
    # Quote basics.
    lotr = LOTR()
    quotes = lotr.quotes(limit=7)
    assert len(quotes) == 7
    quote_6 = quotes[6]
    assert lotr.quotes(id=quote_6.id)[0] == quote_6


def test_movie_quotes():
    # Movie quotes (only works on original 3).
    lotr = LOTR()
    all_movies = lotr.movies()
    two_towers = next(m for m in all_movies if m.name == "The Two Towers")
    movie_quotes = lotr.movie_quotes(id=two_towers.id, limit=11)
    assert len(movie_quotes) == 11
    assert all(isinstance(q, Quote) for q in movie_quotes)
