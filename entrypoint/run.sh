#!/usr/bin/env bash
#
# HEX Entrypoint
#

cd $(dirname "$0")
cd ../

base="/hev"

python3 -m pip install -r $base/requirements.txt
python3 $base/run_HEV.py
