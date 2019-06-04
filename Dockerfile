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
    && rm -f "$driver"

# Install Chrome Browser
RUN browser="google-chrome.deb" \
    && apt update \
    && wget -v -O "$browser" "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" \
    && dpkg -i "$browser" \
    || apt install -f -y \
    && rm -f "$browser"


WORKDIR /hev

COPY core core
COPY external external
COPY libs libs
COPY modules modules
COPY tests tests
COPY web web
COPY run_HEV.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

# run app
CMD ["/bin/bash"]
ENTRYPOINT ["python3", "run_HEV.py"]
