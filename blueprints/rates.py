from flask import Flask, Blueprint, render_template, json, redirect, request
import data.data as rate_data
from datetime import date

# Configure Flask Blueprint
rates_view = Blueprint('rates_view', __name__)


@rates_view.route('/')
def view_rates():
    """Current rates page"""
    rates = rate_data.get_rates()
    date_of_data = date.fromisoformat(rates['date']).strftime("%B %d, %Y")
    return render_template("rates.j2", rates=rates, date_of_data=date_of_data)
