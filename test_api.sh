#!/usr/bin/env bash
curl --data '{"resident": "0100","program": 1}' --request POST --header "Content-Type: application/json" http://localhost:8000/machines/1/run_program/