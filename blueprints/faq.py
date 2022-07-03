from flask import Flask, Blueprint, render_template, json, redirect, request

# Configuration
faq_view = Blueprint('faq_view', __name__)


# View FAQ page
@faq_view.route('/')
def faq():
    return render_template("faq.j2")
