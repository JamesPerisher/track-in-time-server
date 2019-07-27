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
    empty = {"name_first":"", "name_last":"", "gender":"", "year":"", "house":"", "dob":"", "teacher":"", "student_id":""}
    if request.args.to_dict() == {}:
        return render_template("person_form.html", fields=empty)
    base = empty.copy()
    res_data = request.args.to_dict()
    base.update(res_data)

    if "" in [base[x] for x in base]:
        return render_template("person_form.html", error="All fields must be filled.", fields=base)
    return render_template("person_form.html", success="Successfully created user: %s %s"%(base["name_first"], base["name_last"]), fields=empty)
    # TODO: call add to datbase funtion data is in base


c = db.connection()
c.data_entry()
print(c.get_name_info("Person"))

if __name__ == '__main__':
    app.run()
