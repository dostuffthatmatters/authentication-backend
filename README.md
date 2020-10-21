[![Maintainability](https://api.codeclimate.com/v1/badges/87b6138295fbf87fab46/maintainability)](https://codeclimate.com/github/fastsurvey/authentication-backend/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/87b6138295fbf87fab46/test_coverage)](https://codeclimate.com/github/fastsurvey/authentication-backend/test_coverage)

# Authentication API

## Intro

We actually wanted to use an OAuth2 authentication service rather than build these features ourselves - yet again.

However most of the tools we have stumbled accross had on or more of the following issues:

-   Very narrow documentation only suited for specific usecases
-   Rather shitty documentation ...
-   Deep integration with the other services of that provider -> strong dependence on that company
-   Somewhat untrustworthy regarding data security

That is why we are reinventing the wheel yet again :)

<br/>

## About

This OAuth Backend uses Public-Key-Cryptography. There is
a private key that is used to encode(sign) the tokens and
one public key to decode them. By that each resource server
(which has to validate jwt's) doesn't have to share any data
with the authentication backend to verify a token.

We are using the RS256 algorithm to generate a key pair:

```bash
ssh-keygen -t rsa -b 4096 -m PEM -f jwtRS256.key
```

The public key is published via the index route "/".

## Usage

1. Inside your desired python environment run:

```bash
pip install poetry
poetry install
```

2. Run all tests with coverage report with:

```bash
pytest --cov=app --cov-report=term-missing --cov-report=xml ./tests
```

3. Run the app without Docker ...

```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```

... or with Docker:

```bash
docker build -t docker-image .

# Set all required env variables here
docker run -d -p 8080:8080 --env-file .env docker-image
```
