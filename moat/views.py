import requests
import json
from flask import render_template, request, redirect, url_for, flash
from . import app
from . import remove_parens, valid_url, visit_page
from bs4 import BeautifulSoup
import requests
import re

# Choose criteria for job search.
@app.route("/", methods=["GET"])
@app.route("/visit", methods=['GET'])
def visit_get():
    return render_template('whatwiki.html')


@app.route("/", methods=["POST"])
@app.route("/visit", methods=["POST"])
def visit_post(url="https://en.wikipedia.org", topic="",
visited=None):
    topic = request.form['wiki']
    result = visit_page.visit(topic=topic)
    philosophy = "yes"
    if result[-1] != "Philosophy":
        philosophy = "no"
    pretty = [string.replace("_", " ") for string in result]
    result = list(zip(result, pretty))
    return (render_template('results.html', result=result, philosophy=philosophy))