from flask import Flask, Blueprint, render_template, json, redirect, request
import json
import data.data as rate_data

# Configure Flask Blueprint
calc_view = Blueprint('calc_view', __name__)


# View Calculation page
@calc_view.route('/', methods=["POST", "GET"])
def calc():
    print("Test", request)
    # Rate info
    rates = rate_data.get_rates()

    # Render Calculation Page
    if request.method in ["POST", "GET"]:
        pmt_info = pmt_calc(request, rates)
        print(pmt_info, type(pmt_info['addl_pmt']))
        return render_template("calc.j2", pmt_info=pmt_info)


# View Amortization Schedule
@calc_view.route('/amortization-schedule', methods=["POST", "GET"])
def amortization():
    print("Test", request)
    # Rate info
    rates = rate_data.get_rates()

    # Render Amortization Schedule
    if request.method in ["POST", "GET"]:
        pmt_info = pmt_calc(request, rates)
        print(request, pmt_info)
        return render_template("amortization.j2", pmt_info=pmt_info)


def pmt_calc(re, data):
    """Calculate Mortgage Payment(pmt)"""
    if re.method == "GET":
        loan_type, loan_term = "purchase", '30'
        home_price, down_pmt, addl_pmt = 250000, .2, 0
        rate = data[loan_type]['rate'][loan_term]

    if re.method == "POST":
        if re.form.get("calc_info"):
            print("test", re.form, type(re.form))
            loan_type = re.form["loan_type"]
            loan_term = re.form["loan_term"]
            home_price = int(re.form["home_price"])
            down_pmt = int(re.form["down_pmt"]) / 100
            addl_pmt = int(re.form["addl_pmt"])
            rate = data[loan_type]['rate'][loan_term]

    # Calculate info for summary
    loan_amt = (home_price * (1 - down_pmt))
    monthly_pmt = (loan_amt * (rate / 12) /
                   (1 - (1 + rate / 12) ** (-1 * int(loan_term) * 12)))
    monthly_pmt = round(monthly_pmt, 2)
    sum_pmts = int(loan_term) * 12 * monthly_pmt

    # Pass dictionary to template
    pmt_info = {"loan_type": loan_type, "loan_term": loan_term,
                "home_price": home_price, "down_pmt": down_pmt * 100,
                "monthly_pmt": monthly_pmt, "addl_pmt": addl_pmt,
                "rate": rate * 100, "tot_prin": loan_amt,
                "tot_int": sum_pmts - loan_amt, "sum_pmts": sum_pmts}

    pmt_info["amort_info"] = amortization_calc(pmt_info)

    return pmt_info


def amortization_calc(info):
    """Generate information for amortization schedule"""
    print(info)
    loan_term = int(info['loan_term'])
    time = 0
    balance = info['tot_prin']
    payment = info['monthly_pmt']
    principal = 0
    additional = 0
    interest = 0
    tot_int = 0

    amort_info = {'schedule': {}}
    headings = ['principal', 'additional', 'interest', 'balance']
    values = [principal, additional, interest, balance]
    amort_info['schedule'][time] = dict(zip(headings, values))

    while balance > 0:
        time += 1
        interest = round(balance * info['rate'] / (12 * 100), 2)
        tot_int += interest
        additional = info['addl_pmt']
        principal = round(((interest + balance) if time == (loan_term * 12)
                     else min(interest + balance, payment - interest)), 2)
        balance = round(max(0, balance - principal - additional), 2)
        values = [principal, additional, interest, balance]
        amort_info['schedule'][time] = dict(zip(headings, values))

    amort_info['tot_int'] = round(tot_int, 0)
    amort_info['tot_pmt'] = round(tot_int + info['tot_prin'], 0)
    print(amort_info)
    return amort_info
