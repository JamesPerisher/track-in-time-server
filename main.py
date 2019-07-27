from flask import Flask
from flask import render_template, redirect
import json, sqlite3
import time, pytz
import numpy as np
import os


app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/help')
def helpme():
    return render_template("helpme.html")

@app.route('/home')
def home_redirect():
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run()
