from flask import Flask
from flask import render_template, redirect
import json
import time, pytz
import numpy as np
import os
import db_interact.py

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/home')
def home_redirect():
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run()
