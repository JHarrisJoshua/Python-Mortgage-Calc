from flask import Flask, Blueprint, render_template, json, redirect, request
import data.data as rate_data
from datetime import date

# Configuration
rates_view = Blueprint('rates_view', __name__)


# View FAQ page
@rates_view.route('/')
def view_rates():
    # Rate info
    rates = rate_data.get_rates()
    data_date = date.fromisoformat(rates['date']).strftime("%B %d, %Y")
    return render_template("rates.j2", rates=rates, data_date=data_date)
