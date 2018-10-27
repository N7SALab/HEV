#!/usr/bin/env bash
#
# HEX Entrypoint
#

cd $(dirname "$0")
cd ../

base="/hev"

pip3 install -r $base/requirements.txt
python3 $base/run-hev.py
