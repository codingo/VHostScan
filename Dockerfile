FROM ubuntu:latest

RUN mkdir /app

ADD . /app

RUN apt-get update; apt-get install -y python3 python3-pip

RUN cd /app && pip3 install -r test-requirements.txt && python3 setup.py install

ENTRYPOINT ["VHostScan"]
