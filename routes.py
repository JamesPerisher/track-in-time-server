from flask import Flask
from flask import render_template, redirect, make_response, request, url_for
# import logging as log
import json
import time
import pytz
import numpy as np
import os
try:
    import db_interact as db
except (ModuleNotFoundError, ImportError):
    print("Database import error")
import datetime

from input_classes import *

app = Flask(__name__, template_folder='templates')
app.debug = True



# log.basicConfig(filename='%s.log'%__name__, level=log.DEBUG, format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S')


@app.route("/submitform", methods=['POST'])
def submitform():
    print(request.form)
    return make_response(redirect(url_for('.%s'%request.form["id"])))



@app.route("/")
def home():
    return render_template("home.html")


@app.route('/home')
def home_redirect():
    return redirect("/", code=302)


@app.route('/add_student', methods = ["GET","POST"])
def add_student():
    if request.method == "GET":
        elements = [
        input_text("First Name", "name_first"),
        input_text("Last Name", "name_last"),
        input_gender("Gender", "gender"),
        input_yearGroup("Year", "age_group"),
        input_house("Element", "house"),
        input_dob("Date of birth", "dob"),
        input_text("Student id", "stu_id"),
        input_submit("Submit")
        ]
        return render_template("input_template.html", elements=elements)

    if request.method == "POST":
        if check_data(request)[0]:
            # success
            # TODO: call db create function
            return redirect(url_for('.add_student', success="Success passing data."))
        else:
            return redirect(url_for('.add_student', error="All fields are required"))


@app.route('/add_event', methods = ["GET","POST"])
def add_event():
    if request.method == "GET":
        elements = [
        input_text("Event Name", "name"),
        input_gender("Gender", "gender"),
        input_age_group("Age group", "age_group"),
        input_event_type("Event type", "event_type"),
        input_submit("Submit")
        ]
        return render_template("input_template.html", elements=elements)

    if request.method == "POST":
        if check_data(request)[0]:
            # success
            # TODO: call db create function
            return redirect(url_for('.add_event', success="Success passing data."))
        else:
            return redirect(url_for('.add_event', error="All fields are required"))


@app.route('/add_age_groups', methods = ["GET","POST"])
def add_age_groups():
    if request.method == "GET":
        elements = [
        input_dob("Age group start date", "start_date"),
        input_dob("Age group end date", "end_date"),
        input_submit("Submit")
        ]
        return render_template("input_template.html", elements=elements)

    if request.method == "POST":
        if check_data(request)[0]:
            # success
            # TODO: call db create function
            return redirect(url_for('.add_age_groups', success="Success passing data."))
        else:
            return redirect(url_for('.add_age_groups', error="All fields are required"))


@app.route('/add_year_groups', methods = ["GET","POST"])
def add_year_groups():
    if request.method == "GET":
        elements = [
        input_text("Year name", "year_name"),
        input_submit("Submit")
        ]
        return render_template("input_template.html", elements=elements)

    if request.method == "POST":
        if check_data(request)[0]:
            # success
            # TODO: call db create function
            return redirect(url_for('.add_year_groups', success="Success passing data."))
        else:
            return redirect(url_for('.add_year_groups', error="All fields are required"))


@app.route('/cmd')
def cmd():
    try:
        a = eval(request.args.to_dict()["cmd"])
        return {"r": a}
    except Exception as e:
        return e


@app.errorhandler(404)
def error404(error):
    elements = []
    return(render_template("input_template.html", elements=elements))

if __name__ == '__main__':
    app.run()
