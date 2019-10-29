from flask import Flask
from flask import render_template, redirect, make_response, request, url_for
from werkzeug.exceptions import HTTPException

# import logging as log
import json
import time
import pytz
import numpy as np
import os
import secrets as s
try:
    import db_interact as db
except (ModuleNotFoundError, ImportError):
    print("Database import error")
import datetime

from forms import *

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = "".join([s.choice([chr(i) for i in range(32,127)]) for j in range(128)]) # gen random secret probs bad idea
app.debug = True

print("Secret key: %s" %app.config['SECRET_KEY'])

# log.basicConfig(filename='%s.log'%__name__, level=log.DEBUG, format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S')


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/home')
def home_redirect():
    return redirect("/", code=302)


@app.route('/add_student', methods = ["GET","POST"])
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit(): # sucess passing data do stuff
        return redirect('/home')

    return render_template("input_template.html", form=form)



@app.route('/add_event', methods = ["GET","POST"])
def add_event():
    form = AddEvent()

    if form.validate_on_submit(): # sucess passing data do stuff
        return redirect('/home')

    return render_template("input_template.html", form=form)


@app.route('/add_age_groups', methods = ["GET","POST"])
def add_age_groups():
    form = AddAgeGroups()

    if form.validate_on_submit(): # sucess passing data do stuff
        return redirect('/home')

    return render_template("input_template.html", form=form)



@app.route('/cmd')
def cmd():
    try:
        a = eval(request.args.to_dict()["cmd"])
        return {"r": a}
    except Exception as e:
        return e


@app.errorhandler(HTTPException)
def error404(error):
    print(error, type(error))
    error = str(error)
    try:
        return(render_template("error.html", error_num=error.split(":",1)[0], error_txt=error.split(":",1)[1]))
    except IndexError:
        return(render_template("error.html", error_num="Infinity", error_txt="This error SHOULD in theory never be seen by the user."))

if __name__ == '__main__':
    app.run()
