FROM ubuntu:latest

RUN mkdir /app

ADD . /app

RUN apt update; apt install -y python3 python3-pip

RUN cd /app && pip3 install -r test-requirements.txt && python3 setup.py install

ENTRYPOINT ["VHostScan"]
