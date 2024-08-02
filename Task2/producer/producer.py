import requests
from bs4 import BeautifulSoup
from kafka import KafkaProducer
import json
import time
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ENV variables
bootstrap_servers = os.environ.get('KAFKA_BROKER', 'kafka-prod:29092')

while True:
    try:
        # Create a Kafka producer object
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        logger.info(f"Connected to Kafka broker: {bootstrap_servers}")
        break
    except Exception as e:
        logger.error(f"Error connecting to Kafka broker: {e}")
        time.sleep(5)

# Base URL of the website to scrape
base_url = 'https://scrapeme.live/shop/'

# Function to scrape data from the website
def scrape_pokemon_data():
    logger.info("Starting to scrape data from the website.")

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all pokemon products
    products = soup.find_all('li', class_='product')

    data = []
    for product in products:
        name = product.find('h2', class_='woocommerce-loop-product__title').text
        price = product.find('span', class_='woocommerce-Price-amount amount').text

        product_url = product.find('a', href=True)['href']

        # Go Pokemon product detail page
        product_response = requests.get(product_url)
        product_soup = BeautifulSoup(product_response.content, 'html.parser')

        description = product_soup.find('div', class_='woocommerce-product-details__short-description').text.strip()
        stock = product_soup.find('p', class_='stock').text.strip()

        data.append({'name': name, 'price': price, 'description': description, 'stock': stock})

    logger.info("Scraping data completed.")
    return data

# Callback functions for Kafka producer
def on_send_success(record_metadata):
    logger.info(f"Message delivered to {record_metadata.topic} [{record_metadata.partition}] at offset {record_metadata.offset}")

def on_send_error(excp):
    logger.error(f"Message delivery failed: {excp}")

# Function to publish messages to Kafka
def produce_to_kafka(data):
    for item in data:
        producer.send('scraped_data', value=item).add_callback(on_send_success).add_errback(on_send_error)
        time.sleep(1)
    producer.flush()
    logger.info("Finished producing messages to Kafka.")

if __name__ == "__main__":
    scraped_data = scrape_pokemon_data()
    produce_to_kafka(scraped_data)
    logger.info("Producer finished. Exiting...")
