FROM python:3.7.3

ENV http_proxy http://wwwproxy.unimelb.edu.au:8000
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000

RUN mkdir /workspace
WORKDIR /workspace
ADD . /workspace

RUN pip install -r requirements.txt

CMD [ "python", "./getResearchData.py" ]