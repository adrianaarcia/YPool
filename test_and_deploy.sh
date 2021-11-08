#!/bin/bash

echo ""
echo "--------------RUNNING TEST SUITE----------------"
./run_test_suite.sh 

cd web
echo ""
echo "--------------CREATING PRODUCTION BUILD----------------"
python3 build_and_bundle.py
cd ../serverless

echo ""
echo "--------------DEPLOYING PRODUCTION BUILD TO AWS----------------"
sls deploy


