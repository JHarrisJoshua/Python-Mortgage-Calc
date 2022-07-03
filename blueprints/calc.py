from flask import Flask, Blueprint, render_template, json, redirect, request

# Configuration
calc_view = Blueprint('calc_view', __name__)


# View Calculation page
@calc_view.route('/')
def calc():
    return render_template("calc.j2")
