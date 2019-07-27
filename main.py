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
    name_first = request.args.get('name_first')
    name_last = request.args.get('name_last')
    gender = request.args.get('gender')
    year = request.args.get('year')
    house = request.args.get('house')
    dob = request.args.get('dob')
    teacher = request.args.get('teacher')
    student_id = request.args.get('student_id')
    if None in [name_first, name_last, gender, year, house, dob, teacher, student_id] or "" in [name_first, name_last, gender, year, house, dob, teacher, student_id]:
        return render_template("person_form.html", error="All fields must be filled.")
    return render_template("person_form.html", success="Successfully created user")

#db.data_entry()

if __name__ == '__main__':
    app.run()
