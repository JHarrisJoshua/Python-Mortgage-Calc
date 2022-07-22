# Citations for the following program -
# Source URL:  https://github.com/osu-cs340-ecampus/flask-starter-app
# Source URL: https://flask.palletsprojects.com/en/2.1.x/blueprints/
# Source URL: https://getbootstrap.com/
# Source URL: https://icon-icons.com/
# Source URL: https://www.bankrate.com/

from flask import Flask, Blueprint, render_template, json, redirect, request
import os

# Import Flask Blueprints for individual pages
from blueprints.calc import calc_view
from blueprints.rates import rates_view
from blueprints.faq import faq_view

# Configure Flask App
app = Flask(__name__)

# Register Flask Blueprints
app.register_blueprint(calc_view, url_prefix='/calculator')
app.register_blueprint(rates_view, url_prefix='/rates')
app.register_blueprint(faq_view, url_prefix='/faq')


@app.route('/')
def root():
    """Route to home page"""
    return render_template("index.j2")


# Listener for local testing
#if __name__ == "__main__":
#    port = int(os.environ.get('PORT', 9999))
#    app.run(port=port, debug=True)
    