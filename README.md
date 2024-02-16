# Zi Web Counter

This is a simple dockerized web counter solution. Based on the Stack Docker, Python, Fastapi, MongoDB. API is implemented in fastapi, the db Backend is MongoDB and the counter itself is implemented via a get request for a count pixel.

We provide sample HTML implementations using /[Sample.html](sample.html).

**User Privacy** is ensured via hash based Host+Agent annomymization. For implementation details see `makeuuid` in [main.py](main.py).


## Manual Installation

`pip install -r requirements.txt`

## Manual Run

`uvicorn main:app --reload` *start for testing*

## Manual Tests

`cd tests`

`pytests`


## Docker testbuild and run

For local testing, a .env file needs to be created and cocker-compose.yml needs to be altered to use said file.

## Test

`docker compose build test`

`docker compose run --rm test`

## Release

`docker compose build release`

`docker compose push release`
