"""The program represents a microservice to the home loan calculator application.
The microservice provides the average daily rates for various mortgage products
by scraping data from bankrate.com."""

import urllib.request
import os
import pika
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv

# Load environment variables from the .env file
load_dotenv(find_dotenv())

# Set the CLOUDAMPQ URL (URL from Heroku config)
CLOUDAMQP_URL = os.environ.get("CLOUDAMQP_URL")


def main() -> None:
    """
    Remote Procedure Call (RPC) using RabbitMQ and Pika Python Client
    Checks for request, scrapes interest rate data,
    and responds with the file name containing rate data
    """
    params = pika.URLParameters(CLOUDAMQP_URL)
    connection = pika.BlockingConnection(params)

    channel = connection.channel()

    channel.queue_declare(queue='rate_queue')

    def on_request(ch, method, props, body):
        print(f"Received Request: {body.decode()}")

        response = scrape_rates()

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rate_queue', on_message_callback=on_request)

    print(" [x] Awaiting Rate requests")
    channel.start_consuming()


def scrape_rates():
    """Retrieves rate information using
    beautiful soup library.
    https://beautiful-soup-4.readthedocs.io/en/latest/
    """
    # Open URL, read HTML, and scrape tags 
    url = 'https://www.bankrate.com/mortgages/20-year-mortgage-rates'
    html_page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html_page, 'html.parser')

    # Store Rate Data in dictionary
    rate_dict = dict()
    attrib_list = ["Interest Rate", "APR"]
    attrib_info = [""] * 2
    ignore_words = ["Product", "Interest Rate", "APR"]

    # Iterate through html tags and store relevant info
    start, end, idx, percent_count = False, False, 0, 0
    for tag in soup.find_all(['div', 'th', 'td']):
        if str(tag.get('id')) == "purchase":
            start = True
        if percent_count >= 16:
            end = True

        # If statements for handling the different html tags we are looking for
        if start and not end:
            # Gets the two categories of products: purchase and refinance
            if str(tag.name) == 'div':
                if str(tag.get('id')) == "purchase" or str(tag.get('id') == "refinance"):
                    heading = str(tag.get('id'))
                    heading = heading.capitalize()
                    rate_dict[heading] = dict()

            # Gets the product type in terms of length
            if str(tag.name) == 'th':
                rate = str(tag.get_text())
                rate = rate.strip('\n')
                if rate not in ignore_words:
                    rate_dict[heading][rate] = \
                        dict(zip(attrib_list, attrib_info))

            # Gets the actual percentage rates
            if str(tag.name) == 'td':
                rate_dict[heading][rate][attrib_list[idx]] = str(tag.get_text())
                idx = (idx + 1) % 2
                percent_count = percent_count + 1
    return rate_dict

if __name__ == "__main__":
    main()
