#!/usr/bin/env bash
#
# HEX Entrypoint
#

cd $(dirname "$0")
cd ../

base="/hev"

# Install Chrome Driver
driver="chromedriver.zip"
wget -v -O "$driver" https://chromedriver.storage.googleapis.com/2.45/chromedriver_linux64.zip
unzip -o -d /usr/local/bin chromedriver.zip
rm -f "$driver"

# Install Chrome Browser
browser="google-chrome.deb"
apt update
wget -v -O "$browser" "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
dpkg -i "$browser"
apt install -f -y

python3 -m pip install -r $base/requirements.txt
python3 $base/run_HEV.py
