FROM ubuntu:16.04

RUN apt-get -qq update && \
		apt-get -y dist-upgrade
RUN apt-get -y install python3 python3-pip

RUN pip3 install --upgrade pip

# Math libs
RUN pip3 install --upgrade numpy \
		pandas \
		bs4 \
		lxml \
		html5lib \
		beautifulsoup4 \
		requests \
		sklearn \
		pytz \
		psutil \
		logger \
		joblib

# Install Kafka
ENV KAFKA_HOME /usr/local/kafka

# install java + others
RUN apt-get -qq update && apt-get install -y \
  wget \
  openjdk-8-jdk

# install kafka
RUN wget http://apache.cs.utah.edu/kafka/2.0.0/kafka_2.12-2.0.0.tgz && \
  tar -xzf kafka_2.12-2.0.0.tgz && \
  mv kafka_2.12-2.0.0 $KAFKA_HOME

WORKDIR /app/ot

EXPOSE 8080
# start kafka, zookeeper, set up kafka topics and start bash
CMD nohup $KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties & \
  sleep 5 && \
  nohup $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties & \
  sleep 10 && \
  $KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic event-new-game && \
  $KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic event-game-qualified && \
  $KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic event-bet-placed && \
  $KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic event-new-bb-game && \
  $KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic event-bb-game-qualified && \
  $KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic event-error && \
  bash
