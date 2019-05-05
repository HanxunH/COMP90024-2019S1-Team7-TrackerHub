FROM python:3

ADD getResearchData.py /
ADD helper.py /
ADD api_requirements.py /

RUN pip install -r requirements.txt


CMD [ "python", "./getResearchData.py" ]