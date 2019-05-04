FROM ubuntu:16.04
 
RUN apt-get -y update

RUN apt-get install software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get -y update

RUN apt-get install -y python3.7 python-pip

RUN mkdir /code
WORKDIR /code
ADD . /code
RUN pip install -r requirements.txt
EXPOSE 8080
