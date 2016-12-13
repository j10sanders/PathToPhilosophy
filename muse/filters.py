from . import app
from flask import Markup
import mistune as md

@app.template_filter()
def markdown(text):
    return Markup(md.markdown(text,escape=True))

@app.template_filter()
def loactions(location, format):
    if not location:
        return None
    return location[11:-3]