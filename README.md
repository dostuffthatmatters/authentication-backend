[![Maintainability](https://api.codeclimate.com/v1/badges/87b6138295fbf87fab46/maintainability)](https://codeclimate.com/github/fastsurvey/authentication-backend/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/87b6138295fbf87fab46/test_coverage)](https://codeclimate.com/github/fastsurvey/authentication-backend/test_coverage)

# Authentication API

Read the full documentation of this authentication backend in the FastSurvey documentation:

[docs.fastsurvey.io/docs/authentication/api-keys-vs-oauth2](https://docs.fastsurvey.io/docs/authentication/api-keys-vs-oauth2/)

<br/>

## Run locally

1. We are using the `RS256` algorithm. To generate a key pair, run:

```bash
ssh-keygen -t rsa -b 4096 -m PEM -f jwtRS256.key
```

2. Inside your desired python environment run:

```bash
pip install poetry
poetry install
```

3. Run all tests with coverage report with:

```bash
pytest --cov=app --cov-report=term-missing --cov-report=xml ./tests
```

4. Run the app without Docker ...

```bash
uvicorn app:app --host 0.0.0.0 --port 8080 --env-file .env
```

... or with Docker:

```bash
docker build -t <image-name> .

# Set all required env variables here
docker run -d -p 8080:8080 --env-file .env <image-name>
```
