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

## Usage

1. Inside your desired python environment run:

```bash
pip install poetry
poetry install
```

2. Generate a private/public-keypair with:

```bash
ssh-keygen -t rsa -b 4096
```

3. Run all tests with coverage report with:

```bash
pytest --cov=app --cov-report=term-missing --cov-report=xml ./tests
```

4. Run the app (without Docker)

```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```

... or with Docker:

```bash
docker build -t docker-image .

# Set all required env variables here
docker run -d -p 8080:8080 --env-file .env docker-image
```
