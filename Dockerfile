FROM python:3

LABEL maintainer="naisanza@gmail.com"
LABEL description="Hunt Everything"
LABEL dockername="n7salab/hev"

WORKDIR /tmp/hev

COPY drivers.sh .

# Install Chrome Driver
RUN ./drivers.sh

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

# Install python packages
RUN python3 -m pip install -r requirements.txt

# Pytest
# RUN pytest tests

VOLUME "/hev/external/openvpn"
VOLUME "/hev/external/downloads"
VOLUME "/hev/modules/youuuuuuutubedl/files"

# run app
ENTRYPOINT ["python3", "run_hev.py"]
