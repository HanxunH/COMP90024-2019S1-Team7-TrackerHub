FROM python:3.7.3

ENV http_proxy http://wwwproxy.unimelb.edu.au:8000
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD . /code
RUN pip install -r requirement.txt
EXPOSE 8080
CMD [ "python","manage.py","runserver","0.0.0.0:8080" ]