FROM apache/kafka:3.8.0

WORKDIR /opt/kafka

# Includes the steps to create a topic, start producer, publish messages, start consumer and listen to messages
COPY entrypoint.sh .

ENTRYPOINT [ "./entrypoint.sh" ]