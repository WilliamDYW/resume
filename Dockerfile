FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -q && apt-get install -qy \
    curl jq \
    texlive-full \
    gnuplot \
    make git python3-pip\
    && rm -rf /var/lib/apt/lists/*

RUN `which python3` -m pip install Pygments pyyaml pdf2image

COPY ./* /data/
WORKDIR /data
VOLUME ["/data"]