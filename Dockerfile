FROM joyzoursky/python-chromedriver:3.7

RUN pip install selenium==3.8.0
RUN pip install puush.py

RUN mkdir /usr/http-info

COPY screenshot.py /usr/http-info

WORKDIR /usr/http-info

ENV HTTPINFO_URL "https://www.laperlerare972-service.com/wp-includes/Requests/prosoft/officelite.htm"
RUN python screenshot.py
