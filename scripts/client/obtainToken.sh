#!/bin/bash

# Execute from the project root directory with
# 'bash ./scripts/client/obtainToken.sh'

curl -X POST 'http://localhost:8000/token' \
    -H  'accept: application/json' \
    -H  'Content-Type: application/x-www-form-urlencoded' \
    -d 'username=...&password=...' \
    > ./scripts/client/jwt.json
