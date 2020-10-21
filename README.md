[![Maintainability](https://api.codeclimate.com/v1/badges/87b6138295fbf87fab46/maintainability)](https://codeclimate.com/github/fastsurvey/authentication-backend/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/87b6138295fbf87fab46/test_coverage)](https://codeclimate.com/github/fastsurvey/authentication-backend/test_coverage)

# Authentication API

## Intro

... some storytelling coming soon!

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

## Implementing a resource server

On any resource server you need to install:

```
PyJWT = {extras = ["cryptography"], version = "^1.7.1"}
```

... with ...

```
pip install "PyJWT[cryptography]"
```

The public key can be fetched from the associated authentication server.

```python
def check_jwt(token):
    try:
        payload = jwt.decode(
            token, PUBLIC_KEY,
            algorithms=["RS256"]
        )
        assert("exp" in payload)
        if payload["exp"] < datetime.timestamp(datetime.utcnow()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        return payload
    except (AssertionError, Exception):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
```

Following the OAuth2.0 schema the token has to be passed as a header with every private route:

```bash
curl ... \
    -H "Authorization": "bearer <token>"
```

When using FastAPI you can easily use the built in easification:

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

...

@app.get("/account")
async def account_route(
    access_token: str = Depends(oauth2_scheme)
):
    ...
```
