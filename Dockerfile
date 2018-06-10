FROM ubuntu:16.04

RUN apt-get -qq update && \
		apt-get -y dist-upgrade
RUN apt-get -y install python3 python3-pip

RUN pip3 install --upgrade pip

# Math libs
RUN pip3 install --upgrade numpy \
		scipy \
		pandas \
		bs4 \
		lxml \
		beautifulsoup4 \
		requests \
		sklearn \
		pytz \
		pprint \
		psutil

WORKDIR /app/ot
		
EXPOSE 8080
CMD bash