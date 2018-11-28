FROM joyzoursky/python-chromedriver:3.7

# Install dependencies
RUN pip install selenium==3.8.0
RUN pip install browsermob-proxy

RUN apt update
RUN apt install default-jre unzip -y

WORKDIR /
RUN mkdir info/
COPY getinfo.py /getinfo.py

# Download browsermob and setup proxy
RUN wget https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip
RUN unzip browsermob-proxy-2.1.4-bin.zip

ENV HTTPINFO_BMP_PATH "./browsermob-proxy-2.1.4/bin/browsermob-proxy"

ENTRYPOINT ["python", "getinfo.py"]
#CMD ["https://example.com"]
