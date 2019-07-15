FROM python:3

LABEL maintainer="naisanza@gmail.com"
LABEL description="Hunt Everythning"
LABEL dockername="skynet/hev"
LABEL dockertag="0.1"
LABEL version="0.1"


WORKDIR /tmp

# Install Chrome Driver
RUN driver="chromedriver.zip" \
    && wget -v -O "$driver" https://chromedriver.storage.googleapis.com/2.45/chromedriver_linux64.zip \
    && unzip -o -d /usr/local/bin chromedriver.zip \
    && rm -rf *

# Install Chrome Browser
RUN browser="google-chrome.deb" \
    && apt update \
    && wget -v -O "$browser" "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" \
    && dpkg -i "$browser" \
    || apt install -f -y \
    && apt autoclean \
    && rm -rf * 


WORKDIR /hev

COPY core core
COPY external external
COPY modules modules
COPY tests tests
COPY web web
COPY run_hev.py .
COPY requirements.txt .
COPY hev.conf .

# Install python packages
RUN python3 -m pip install -r requirements.txt

VOLUME "/hev/external/openvpn"

# run app
ENTRYPOINT ["python3", "run_hev.py"]

