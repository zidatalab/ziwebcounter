# Simple webcounte with fastapi

This should provide a simple web counter solution via docker. API is implemented in fastapi, db is MongoDB and the counter itself is implemented via a count pixel.

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

`docker-compose build test`
`docker-compose run --rm test`

## Release

`docker-compose build release`
