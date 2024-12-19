#!/usr/bin/env bash

curl -X 'POST' \
  'http://127.0.0.1:8000/log/' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "johndoe",
  "device_id": "abc123",
  "ip": "10.168.1.10",
  "date": "2024-12-19T00:00:00",
  "login_success": true
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/log/' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "johndoe",
  "device_id": "abc123",
  "ip": "192.168.1.10",
  "date": "2024-12-19T00:00:00",
  "login_success": true
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/log/' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "johndoe",
  "device_id": "absdsc123",
  "ip": "214.168.1.10",
  "date": "2024-12-19T00:00:00",
  "login_success": false
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/log/' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "janedoe",
  "device_id": "absdc123",
  "ip": "192.168.1.10",
  "date": "2024-12-19T00:00:00",
  "login_success": true
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/log/' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "janeXdoe",
  "device_id": "absdc123",
  "ip": "192.168.1.120",
  "date": "2024-12-12T00:00:00",
  "login_success": false
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/log/' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "johndoe",
  "device_id": "abc123",
  "ip": "10.168.1.10",
  "date": "2024-12-19T00:00:00",
  "login_success": false
}'
