# Imports
from datetime import date
import json
import os


def get_rates():
    """Check if rates are from today, update rate information.
    TODO: use microservice to get current rates
    """
    # Datetime
    date_today = str(date.today())

    path = os.path.join(os.path.dirname(__file__))
    with open(path + '/' + 'rates.json') as infile:
        rate_data = json.load(infile)

    if rate_data['date'] == date_today:
        print('No Update Needed')
    else:
        print('Update')

    return rate_data
