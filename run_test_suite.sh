#!/bin/bash

cd serverless/flask-server
echo "------RUNNING SERVER SIDE TESTS------"
python3 -m pytest . -v

cd ../..


