#!/usr/bin/env bash

# selenium requirements

cd $(dirname "$0")

set -xe

# Install Chrome Driver
driver="chromedriver.zip"
wget -v -O "$driver" "https://chromedriver.storage.googleapis.com/78.0.3904.11/chromedriver_linux64.zip"
unzip -o -d /usr/local/bin chromedriver.zip
chmod +x /usr/local/bin/chromedriver
rm -f "$driver"

# Install Chrome Browser
browser="google-chrome.deb"
apt update
wget -v -O "$browser" "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
dpkg -i "$browser"
apt install -f -y
rm -f "$browser"
