FROM joyzoursky/python-chromedriver:3.7

RUN pip install selenium==3.8.0
RUN pip install puush.py
RUN pip install browsermob-proxy

RUN apt update
RUN apt install default-jre unzip -y

RUN mkdir /usr/http-info
WORKDIR /usr/http-info

COPY screenshot.py /usr/http-info

RUN wget https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip
RUN unzip browsermob-proxy-2.1.4-bin.zip

ENV HTTPINFO_BMP_PATH "./browsermob-proxy-2.1.4/bin/browsermob-proxy"
ENV HTTPINFO_PUUSHAPI "[redacted]"
ENV HTTPINFO_URL "https://google.com"
RUN python screenshot.py
