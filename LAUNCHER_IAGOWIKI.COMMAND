#!/bin/sh
echo Starting Wiki
export PYTHONPATH=$(dirname $0)/libs:$(dirname $0)/src/
cd $(dirname $0)/src
python -W ignore ./wiki.py
echo Done