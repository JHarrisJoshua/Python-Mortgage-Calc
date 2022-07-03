# Citations for the following program -
# Source URL:  https://github.com/osu-cs340-ecampus/flask-starter-app
# Source URL: https://flask.palletsprojects.com/en/2.1.x/blueprints/
# Source URL: https://stackoverflow.com/questions/24579581/how-to-do-confirmation-in-a-form-before-submit
# Source URL: https://getbootstrap.com/
# Source URL: https://icon-icons.com/

# Imports
from flask import Flask, Blueprint, render_template, json, redirect, request
import os

# Import Flask Blueprints for individual pages
from blueprints.calc import calc_view
from blueprints.faq import faq_view

# Configure Flask App
app = Flask(__name__)

# Register Flask Blueprints
app.register_blueprint(calc_view, url_prefix='/calculator')
app.register_blueprint(faq_view, url_prefix='/faq')


# Route to home page
@app.route('/')
def root():
    return render_template("index.j2")


# Listener
if __name__ == "__main__":
    # Local Testing
    port = int(os.environ.get('PORT', 9999))
    app.run(port=port, debug=True)
    