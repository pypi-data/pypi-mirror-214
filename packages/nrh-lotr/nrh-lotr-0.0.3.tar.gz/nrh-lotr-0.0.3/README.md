# Lord of the Rings SDK

Author: Nathanial Hapeman

Simple SDK for exploring 2 endpoints from [the-one-api](https://the-one-api.dev/):

- LotR movies
  - Supports fetching by id
- LotR quotes
  - Supports fetching quotes by id
- LotR movie quotes
  - Supports fetching quotes by movie id

All LotR sdk functions support limit and offset.

The data pulled from the external api will be loaded into pydantic models
which have the added benefit of validating the data and being easy to declare.

## Installation

Using python>=3.9: `pip install nrh-lotr`

## Usage

```py
# First grab an api key from: https://the-one-api.dev/documentation#3
# Then put it in an env var like: `export API_KEY=SOME_API_KEY`
# Or insert it directly into the LOTR class as depicted below
from lotr import LOTR, Movie, Quote

# Movie basics.
lotr = LOTR("YOUR_API_KEY")
# lotr = LOTR() # if using env var
movies = lotr.movies(limit=5)
assert len(movies) == 5
movie_3 = movies[3]
assert lotr.movies(id=movie_3.id)[0] == movie_3

# Quote basics.
lotr = LOTR()
quotes = lotr.quotes(limit=7)
assert len(quotes) == 7
quote_6 = quotes[6]
assert lotr.quotes(id=quote_6.id)[0] == quote_6

# Movie quotes (only works on original 3).
lotr = LOTR()
all_movies = lotr.movies()
two_towers = next(m for m in all_movies if m.name == "The Two Towers")
movie_quotes = lotr.movie_quotes(id=two_towers.id, limit=11)
assert len(movie_quotes) == 11
assert all(isinstance(q, Quote) for q in movie_quotes)
```

## Developing from source? Install like:

```sh
python3 -m venv lotr
source ./lotr/bin/activate
python -m pip install -e .
```

## Original Prompt

Create these endpoints:

- /movie
- /movie/{id}
- /movie/{id}/{quote}
- /quote
- /quote/{id}

Deploy to package manager like: npm, pip, maven, etc...

Fill out design.md
