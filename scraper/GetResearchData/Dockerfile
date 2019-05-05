FROM python:3

ADD getResearchData.py /
ADD untitled.py /
ADD api_requirements.py /


RUN pip install GetOldTweets3
RUN pip install bs4
RUN pip install requests
RUN pip install requests.auth
RUN pip install pillow
RUN pip install datetime

CMD [ "python3", "./getResearchData.py" ]