from datetime import date
import json
import os


def get_rates():
    """
    Get rate information and return data
    """
    # Find relative path to JSON file and open
    path = os.path.join(os.path.dirname(__file__))
    with open(path + '/' + 'rates.json') as infile:
        rate_data = json.load(infile)
        check_rate_date(rate_data)
    return rate_data


def check_rate_date(rate_data):
    """Check if rates are from today, update rate information if needed.
    TODO: use microservice to get current rates
    """
    # TODO: update rates programmatically via microservice
    if rate_data['date'] == str(date.today()):
        print('No Update Needed')
    else:
        print('Update')
