import logging
import json
import os
import time
from kafka import KafkaConsumer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ENV variables
bootstrap_servers = os.environ.get('KAFKA_BROKER', 'kafka-cons:29093')
kafka_topic_name = os.environ.get('KAFKA_TOPIC_NAME', 'scraped_data')


while True:
    try:
        logger.info(f"Connecting to Kafka broker: {bootstrap_servers}...")

        # Create a Kafka consumer object
        consumer = KafkaConsumer(
            kafka_topic_name,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
        )

        logger.info(f"Connected to Kafka broker: {bootstrap_servers}")
        break
    except Exception as e:
        logger.error(f"Error connecting to Kafka broker: {e}.")
        time.sleep(5)

# File that will store the scraped data
output_file = os.environ.get('DATA_FILE', '/data/scraped_data.json')

# Function to write the message to the file
def handle_message(message):
    if not message:
        return
    with open(output_file, 'a') as f:
        json.dump(message.value, f)
        f.write('\n')
    logger.info(f"Saved: {message.value}")

if __name__ == "__main__":
    try:
        # Create the file
        with open(output_file, 'w') as f:
            logger.info("File created.")
            pass
        logger.info("Consuming messages...")
        while True:
            msg = consumer.poll(timeout_ms=1000)
            # Read messages from the Kafka topic if messages are available
            if msg:
                for tp, messages in msg.items():
                    for message in messages:
                        logger.debug(f"Message received: {message.value}")
                        handle_message(message)
    except Exception as e:
        logger.error(f"Error consuming message: {e}")
    finally:
        consumer.close()
