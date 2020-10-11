
# Execute from the project root directory with
# 'bash ./scripts/client/obtainToken.bash'

curl -X POST 'http://localhost:8000/token' \
    -H  'accept: application/json' \
    -H  'Content-Type: application/x-www-form-urlencoded' \
    -d 'username=...&password=...' \
    > ./scripts/client/jwt.json
