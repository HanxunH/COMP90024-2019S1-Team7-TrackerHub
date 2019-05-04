FROM ubuntu:16.04

ENV http_proxy http://wwwproxy.unimelb.edu.au:8000
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000

RUN apt-get -y update

RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get -y update

RUN apt-get install -y python3.7 python3-pip
RUN pip3 install --upgrade pip

RUN mkdir /code
WORKDIR /code
ADD . /code
RUN pip3 install -r requirement.txt
EXPOSE 8080
