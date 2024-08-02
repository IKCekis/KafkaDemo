# KafkaDemo
This repository contains the implementation of a task to set up Apache Kafka using Docker

# How to start
## Task 1:
1. First we need to build the dockerfile by using the following command: `docker build -t kafka-task1 .`

2. Then we need to run the docker container by using the following command: `docker run kafka-task1`

## Task 2:
1. To run the docker-compose file in background, we need to use the following command: `docker-compose up -d`

2. To check the logs of the producer container, we need to use the following command: `docker-compose logs -f producer`

3. To check the logs of the consumer container, we need to use the following command: `docker-compose logs -f consumer`

4. To stop the docker-compose file and remove the volumes, we need to use the following command: `docker-compose down --volumes`
