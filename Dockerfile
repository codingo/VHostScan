FROM python:3-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt update && apt install -y gcc g++ && \
	pip3 install --no-cache-dir -r requirements.txt && \
	apt remove -y gcc g++ && \
	apt autoremove -y && \
	rm -rf /var/lib/apt/lists/*

COPY . .

RUN python setup.py install

ENTRYPOINT ["VHostScan"]
