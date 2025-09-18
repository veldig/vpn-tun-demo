FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 python3-pip iproute2 iputils-ping net-tools \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install python-pytun cryptography
WORKDIR /home/app