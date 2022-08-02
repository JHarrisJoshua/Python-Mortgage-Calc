from flask import Flask, Blueprint, render_template, json, redirect, request
import json
import data.data as rate_data

# Configure Flask Blueprint
calc_view = Blueprint("calc_view", __name__)

# Default Values for GET method
PRICE, DOWN = 250000, 20


@calc_view.route("/", methods=["POST", "GET"])
def calc():
    """View Payment (pmt) Calculation page"""
    rates = rate_data.get_rates()

    if request.method in ["POST", "GET"]:
        payment_info = pmt_calc_route(request, rates)
        return render_template("calc.j2", pmt_info=payment_info)


@calc_view.route("/amortization-schedule", methods=["POST"])
def amortization():
    """View Amortization Schedule Page"""
    rates = rate_data.get_rates()

    if request.method == "POST":
        payment_info = pmt_calc_route(request, rates)
        return render_template("amortization.j2", pmt_info=payment_info)


def pmt_calc_route(re, rates):
    """Generate Mortgage Payment(pmt) info depending on route"""
    pmt_info = create_pmt_dict() if request.method == "GET" \
        else get_post_info(re)
    pmt_info = pmt_calc(pmt_info, rates)
    return pmt_info


def create_pmt_dict():
    """ Helper method. Generates a dictionary with default values
    to store payment info"""
    pmt_info = {"loan_type": "purchase", "loan_term": "30",
                "home_price": PRICE, "down_pmt": DOWN, "monthly_pmt": 0,
                "extra_pmt": 0, "rate": 0, "total_principal": 0.0,
                "total_interest": 0, "sum_pmts": 0}
    return pmt_info


def get_post_info(re):
    """Helper Method. Retrieves info from HTML form."""
    pmt_info = create_pmt_dict()

    if re.form.get("calc_info"):
        pmt_info["loan_type"] = re.form["loan_type"]
        pmt_info["loan_term"] = re.form["loan_term"]
        pmt_info["home_price"] = int(re.form["home_price"])
        pmt_info["down_pmt"] = int(re.form["down_pmt"])
        pmt_info["extra_pmt"] = int(re.form["extra_pmt"])
    return pmt_info


def pmt_calc(pmt_info, rates):
    """Populate Payment(pmt) info for Summary"""
    rate = rates[pmt_info["loan_type"]]["rate"][pmt_info["loan_term"]]
    loan_info = pmt_info_helper(pmt_info, rate, pmt_info["loan_term"])
    payment, sum_pmts, loan_amt, total_interest = loan_info

    pmt_info["monthly_pmt"], pmt_info["sum_pmts"] = payment, sum_pmts
    pmt_info["total_principal"] = loan_amt
    pmt_info["total_interest"], pmt_info["rate"] = total_interest, rate * 100
    pmt_info["amort_info"] = amortization_calc(pmt_info)
    return pmt_info


def pmt_info_helper(info, rate, loan_term) -> tuple:
    """Helper Method. Monthly Payment Calculation. """
    loan_amt = (info["home_price"] * (1 - info["down_pmt"]/100))
    payment = round(loan_amt * (rate / 12) /
                    (1 - (1 + rate / 12) ** (-1 * int(loan_term) * 12)), 2)

    sum_pmts = int(loan_term) * 12 * payment
    total_interest = sum_pmts - loan_amt
    return payment, sum_pmts, loan_amt, total_interest


def payment_number_info(values):
    """Formats info for each payment for amortization schedule dictionary"""
    headings = ["principal", "additional", "interest", "balance"]
    return dict(zip(headings, values))


def amortization_calc(info):
    """Generate dictionary with amortization schedule info"""
    amort_info, values = {"schedule": {}}, [0, 0, 0, info["total_principal"]]
    amort_info, total_interest = amortization_schedule(values, amort_info, info)
    amort_info["total_interest"] = round(total_interest, 0)
    amort_info["total_pmt"] = round(total_interest + info["total_principal"], 0)
    return amort_info


def amortization_schedule(values, amort_info, info, total_interest=0):
    """Helper Method. Iterates through payment schedule until balance is zero"""
    principal, extra, interest, balance = values

    time = 0
    while balance > 0 or interest > 0:
        values = [principal, extra, interest, balance]
        amort_info["schedule"][time] = payment_number_info(values)
        principal, extra, interest, balance = calc_values(values, info, time+1)
        time, total_interest = time + 1, total_interest + interest
    return amort_info, total_interest


def calc_values(values, info, time):
    """Helper. Update principal, additional payment, interest, balance values"""
    principal, extra, interest, balance = values
    loan_term, payment = int(info["loan_term"]), info["monthly_pmt"]
    interest = round(balance * info["rate"] / (12 * 100), 2)
    extra = info["extra_pmt"]
    principal = round(min(interest + balance, payment - interest)
                      if time != (loan_term * 12) else (interest + balance), 2)
    balance = round(max(0, balance - principal - extra), 2)
    return principal, extra, interest, balance
