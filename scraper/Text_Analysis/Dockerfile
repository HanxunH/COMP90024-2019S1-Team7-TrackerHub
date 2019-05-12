FROM fokkodriesprong/docker-pyspark

ENV http_proxy http://wwwproxy.unimelb.edu.au:8000
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000

RUN mkdir /workspace
WORKDIR /workspace
ADD . /workspace

RUN python -V

CMD [ "python", "./stream_analyzer.py"]