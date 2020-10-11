#!/bin/bash

access_token="..."

curl -X GET 'http://localhost:8000/profile' \
    --header "Authorization: Bearer "$access_token
