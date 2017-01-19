import os

from flask import Flask

app = Flask(__name__)

from . import views

app.secret_key = 'super secret key'