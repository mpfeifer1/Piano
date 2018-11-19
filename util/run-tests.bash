#!/usr/bin/env bash

# if any command inside script returns error, exit and return that error 
set -e

# magic line to ensure that we're always inside the root of our application,
# no matter from which directory we'll run script
# thanks to it we can just enter `./scripts/run-tests.bash`
cd "${0%/*}/../src/test"

echo "Running tests"
echo "............................" 
python3.5 grammartests.py
python3.5 semantictests.py
