from flask import Flask
from flask import render_template, redirect
from flask import request
import json
import time, pytz
import numpy as np
import os
import db_interact as db

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
    print(request.args.get('page', default = 1, type = int))
    return render_template("person_form.html")


c = db.connection()
c.data_entry()


if __name__ == '__main__':
    app.run()
