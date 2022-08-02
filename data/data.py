from datetime import date
import time
import json
import os
from urllib import response
import uuid
import ast
import pika
from dotenv import load_dotenv, find_dotenv

# Load environment variables from the .env file
load_dotenv(find_dotenv())

# Set the CLOUDAMPQ URL (URL from Heroku config)
CLOUDAMQP_URL = os.environ.get("CLOUDAMQP_URL")

class RateRpcClient(object):

    def __init__(self):
        self.params = pika.URLParameters(CLOUDAMQP_URL)
        self.connection = pika.BlockingConnection(self.params)

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rate_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(body))
        self.connection.process_data_events(time_limit=None)
        return self.response


def get_rates():
    """
    Get rate information and return data
    """
    # Find relative path to JSON file and open
    path = os.path.join(os.path.dirname(__file__))
    with open(path + "/" + "rates.json") as infile:
        rate_data = json.load(infile)
    return check_rate_date(rate_data, path)


def check_rate_date(rate_data, path):
    """
    Check if rates are from today, update rate information if needed.
    """
    if rate_data["date"] == str(date.today()):
        print("No Update Needed")
        return rate_data
    print("Update Needed")
    return call_microservice(rate_data, path)


def call_microservice(rate_data, path):
    """Request rates from microservice"""
    rate_rpc = RateRpcClient()
    new_rates = rate_rpc.call("Get Rates")
    new_rates = ast.literal_eval(new_rates.decode('utf-8'))
    return process_file(new_rates, rate_data, path)


def process_file(new_rates, rate_data, path):
    """Process JSON file with new rates"""
    rate_data["date"] = str(date.today())
    rate_data = update_rate_date(rate_data, new_rates)
    dump_json(rate_data, path)
    return rate_data


def update_rate_date(rate_data, new_rates):
    """Iterate through JSON file with new rates and store locally"""
    for product in new_rates.keys():
        for term in new_rates[product].keys():
            for rate in new_rates[product][term].keys():
                rate_key = rate.lower().replace("interest ", "")
                new_rate = new_rates[product][term][rate]
                form_rate = round(float(new_rate.replace("%", "")) / 100, 4)
                rate_data[product.lower()][rate_key][term[:2]] = form_rate
    return rate_data


def dump_json(rate_data, path):
    """Save out new rates to local persistence"""
    with open(path + "/" + "rates.json", "w") as outfile:
        json.dump(rate_data, outfile, indent=4)
