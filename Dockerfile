FROM python:3

LABEL maintainer="naisanza@gmail.com"
LABEL description="Hunt Everythning"
LABEL dockername="n7salab/hev"

WORKDIR /tmp

# Install Chrome Driver
RUN driver="chromedriver.zip" \
    && wget -v -O "$driver" "https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_linux64.zip" \
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

# Install wifite2
RUN git clone https://github.com/derv82/wifite2 \
    && cd wifite2 \
    && python3 setup.py install

WORKDIR /hev

COPY core core
COPY external external
COPY modules modules
COPY tests tests
COPY web web
COPY run_hev.py .
COPY requirements.txt .
COPY hev-conf.json .

# Install python packages
RUN python3 -m pip install -r requirements.txt

# Pytest
# RUN pytest tests

VOLUME "/hev/external/openvpn"
VOLUME "/hev/external/downloads"
VOLUME "/hev/modules/youuuuuuutubedl/files"

# run app
ENTRYPOINT ["python3", "run_hev.py"]
