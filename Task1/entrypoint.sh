#!/bin/sh

echo '***Starting Zookeeper***'
echo ''
bin/zookeeper-server-start.sh config/zookeeper.properties > /dev/null 2>&1 &

# Wait for Zookeeper to start
echo '***Waiting for Zookeeper to start***'
echo ''
while ! nc -z localhost 2181; do
  sleep 1
done

echo '***Starting Kafka***'
echo ''
bin/kafka-server-start.sh config/server.properties > /dev/null 2>&1 &

# Wait for Kafka to start
echo '***Waiting for Kafka to start***'
echo ''
while ! nc -z localhost 9092; do
  sleep 1
done

echo '***Creating Kafka Topic***'
echo ''

# Create a topic
bin/kafka-topics.sh --create --topic shipment-events --bootstrap-server localhost:9092
echo ''

echo '***Producing Messages***'
echo ''

# Start the producer and send messages
echo "Your Order Has Been Received" > producer0.txt
echo "Your Order Has Been Shipped" > producer1.txt
echo "Your Order Has Been Delivered" > producer2.txt
bin/kafka-console-producer.sh --topic shipment-events --bootstrap-server localhost:9092 < producer0.txt
bin/kafka-console-producer.sh --topic shipment-events --bootstrap-server localhost:9092 < producer1.txt
bin/kafka-console-producer.sh --topic shipment-events --bootstrap-server localhost:9092 < producer2.txt

echo '***Starting Consumer***'
echo ''

# Start the consumer
bin/kafka-console-consumer.sh --topic shipment-events --from-beginning --bootstrap-server localhost:9092 > consumer.txt &

sleep 3

echo ' -----------------------------------------------'
echo '|     Consumer is running in the background.    |'
echo '| Check the consumer.txt file for the output.   |'
echo ' -----------------------------------------------'
echo ''
echo 'Output of consumer.txt:'
cat consumer.txt
