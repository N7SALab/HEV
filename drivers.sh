#!/usr/bin/env bash

# selenium requirements

cd $(dirname "$0")

set -xe

# Install Chrome Driver 80
driver="chromedriver.zip"
wget -q -O "$driver" "https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip"
unzip -o -d /usr/local/bin "$driver"
chmod +x /usr/local/bin/chromedriver
rm -f "$driver"

# Install Chrome Browser 80.0.3987.132
browser="google-chrome.deb"
wget -O "$browser" "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
dpkg -i "$browser" || apt update
apt install -f -y
rm -f "$browser"
