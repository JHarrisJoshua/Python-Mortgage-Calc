from flask import Flask, Blueprint, render_template, json, redirect, request

# Configure Flask Blueprint
faq_view = Blueprint("faq_view", __name__)


@faq_view.route("/")
def faq():
    """Frequently Asked Questions (FAQ) Page"""
    return render_template("faq.j2")
