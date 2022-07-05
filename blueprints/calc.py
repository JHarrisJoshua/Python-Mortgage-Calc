from flask import Flask, Blueprint, render_template, json, redirect, request
import json

import data.data as rate_data

# Configuration
calc_view = Blueprint('calc_view', __name__)


# View Calculation page
@calc_view.route('/', methods=["POST", "GET"])
def calc():
    # Rate info
    rates = rate_data.get_rates()

    # Render Calculation Page
    if request.method in ["POST", "GET"]:
        pmt_info = pmt_calc(request, rates)
        return render_template("calc.j2", pmt_info=pmt_info)


def pmt_calc(re, data):
    """Calculate Mortgage Payment"""
    if re.method == "GET":
        loan_type, loan_term = "purchase", '30'
        home_price, down_pmt = 250000, .2
        rate = data[loan_type]['rate'][loan_term]

    if re.method == "POST":
        if re.form.get("calc_info"):
            loan_type = re.form["loan_type"]
            loan_term = re.form["loan_term"]
            home_price = int(re.form["home_price"])
            down_pmt = int(re.form["down_pmt"]) / 100
            rate = data[loan_type]['rate'][loan_term]

    # Calculate info for summary
    loan_amt = (home_price * (1 - down_pmt))
    monthly_pmt = (loan_amt * (rate / 12) /
                   (1 - (1 + rate / 12) ** (-1 * int(loan_term) * 12)))
    monthly_pmt = round(monthly_pmt, 2)
    sum_pmts = int(loan_term) * 12 * monthly_pmt

    # Pass dictionary to template
    pmt_info = {
        "loan_type": loan_type,
        "loan_term": loan_term,
        "home_price": home_price,
        "down_pmt": down_pmt * 100,
        "monthly_pmt": monthly_pmt,
        "rate": rate * 100,
        "tot_prin": loan_amt,
        "tot_int": sum_pmts - loan_amt,
        "sum_pmts": sum_pmts
    }
    return pmt_info
