from flask import Flask
from flask import render_template, redirect
from flask import request
import json, sqlite3
import time, pytz
import numpy as np
import os
import db_interact

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/home')
def home_redirect():
    return redirect("/", code=302)

@app.route('/add_person')
def add_person():
    print(request.args)
    return render_template("person_form.html")


if __name__ == '__main__':
    app.run()
