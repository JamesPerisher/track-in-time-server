#!/usr/bin/python3

# This file is part of Track In Time Server.
#
# Track In Time Server is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Track In Time Server is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Track In Time Server.  If not, see <https://www.gnu.org/licenses/>.

from flask import Flask
from flask import render_template, redirect, make_response, request, url_for, flash
from werkzeug.exceptions import HTTPException

# import logging as log
import os
import time
import json
import pytz
import datetime
import numpy as np
import secrets as s

from forms import *

try:
    import db_interact as custom_db
except (ModuleNotFoundError, ImportError):
    print("Database import error")


app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = "".join([s.choice([chr(i) for i in range(32,127)]) for j in range(128)]) # gen random secret probs bad idea
print("Secret key: %s" %app.config['SECRET_KEY'])

app.db = custom_db.connection()


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/home')
def home_redirect():
    return redirect("/", code=302)

@app.route('/favicon.ico')
def favicon():
    return redirect("static/images/favicon.ico")

@app.route("/license")
def license():
    return render_template("license.html")

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


@app.route("/search")
def search():
    return render_template("index.html", title="search", indexes=["search/user", "search/event"])

@app.route('/search/user', methods = ["GET","POST"])
def search_user(): # TODO: add house to user table in return
    form = SearchUserForm()

    if form.validate_on_submit(): # sucess passing data
        users = app.db.get_participant_info(form.data['search'], search_type=form.data['result'])
        results = [("%s %s"%(x[2], x[1]), x[4], x[6].split(" ")[0], url_for('user_info', name_first=x[2], name_last=x[1], house=x[5], gender=x[3], year=x[4], dob=x[6])) for x in users] # # DEBUG: dict other than m/f
        flash(results)

    return render_template("user_search.html", form=form)

@app.route('/search/event', methods = ["GET","POST"])
def search_event(): # TODO: add house to user table in return
    form = SearchEventForm()

    if form.validate_on_submit(): # sucess passing data
        event = app.db.get_event_info(form.data['search'], search_type=form.data['result'])
        results = [(x[2], x[3], x[5], url_for("event_info", name=x[2], type=x[3], gender=x[5], id = x[0])) for x in event]
        flash(results)

    return render_template("event_search.html", form=form)


@app.route('/add_student', methods = ["GET","POST"])
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit(): # sucess passing data
        return redirect('/home')

    return render_template("input_template.html", form=form)


@app.route('/add_event', methods = ["GET","POST"])
def add_event():
    form = AddEvent()

    if form.validate_on_submit(): # sucess passing data
        return redirect('/home')

    return render_template("input_template.html", form=form)

@app.route("/user_info")
def user_info():
    return render_template("user_info.html")

@app.route("/event_info")
def event_info():
    return render_template("event_info.html")

@app.route("/download")
def download():
    return render_template("download_template.html", name="fancy name", data=[("Zip","/hello"),("Zip","/hello"),("Zip","/hello"),("Zip","/hello")])

@app.route("/results")
def results():
    return render_template("results.html", data=[("dave", "10000"), ("dave", "10000"), ("dave", "10000"), ("dave", "10000"), ("dave", "10000"), ], event_name="100m sprint", gender="attack helicopter", year="10")

@app.route("/events")
def events():
    return render_template("results.html", data=[("100m sprint", "attack helicopter", ""), ("dave", "10000"), ("dave", "10000"), ("dave", "10000"), ("dave", "10000"), ], event_name="100m sprint", gender="attack helicopter", year="10")



@app.context_processor
def utility_processor():
    def get_event_stats(id):
        out = []
        for i in app.db.get_results_from_event(id):
            user = app.db.get_participant_info(i[1], "db_id")[0]
            out.append(("%s %s"%(user[2], user[1]), user[4], user[6].split(" ")[0], i[3], url_for('user_info', name_first=user[2], name_last=user[1], house=user[5], gender=user[3], year=user[4], dob=user[6])))

        out.sort(key = lambda x: x[3], reverse=True)
        return out
    return dict(get_event_stats=get_event_stats)

if __name__ == '__main__':
    app.run(debug = True, use_reloader=True)
