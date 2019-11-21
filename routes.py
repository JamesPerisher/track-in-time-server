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
from werkzeug.datastructures import ImmutableMultiDict

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, HiddenField, RadioField
from wtforms.validators import InputRequired

# import logging as log
import os
import time
import json
import pytz
import datetime
import numpy as np
import secrets as s
import importlib

import forms

import db_interact as custom_db


app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = "".join([s.choice([chr(i) for i in range(32,127)]) for j in range(128)]) # gen random secret probs bad idea
print("Secret key: %s" %app.config["SECRET_KEY"])

app.form_update = lambda : importlib.reload(forms)
app.db = custom_db.connection(app=app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/home")
def home_redirect():
    return redirect("/", code=302)

@app.route("/favicon.ico")
def favicon():
    return redirect("static/images/favicon.ico")

@app.route("/license")
def license():
    return render_template("license.html")

@app.route("/donate")
def donate():
    return redirect("https://www.paypal.me/pauln07/5USD")

@app.route("/cmd")
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
        return render_template("error.html", error_num=error.split(":",1)[0], error_txt=error.split(":",1)[1])
    except IndexError:
        return render_template("error.html", error_num="Infinity", error_txt="This error SHOULD in theory never be seen by the user.")


@app.route("/search_user", methods = ["GET","POST"])
def search_user():
    form = forms.SearchUserForm()

    if form.validate_on_submit(): # sucess passing data
        users = app.db.get_participant_info(form.data["search"], search_type=form.data["result"])
        results = [("%s %s"%(x[2], x[1]), x[3], x[4], x[5], x[6].split(" ")[0], url_for("user_info", id=x[0], name_first=x[2], name_last=x[1], house=x[5], gender=x[3], year=x[4], dob=x[6])) for x in users] # # DEBUG: dict other than m/f
        flash(results)

    return render_template("user_search.html", form=form)

@app.route("/search_event", methods = ["GET","POST"])
def search_event():
    form = forms.SearchEventForm()

    if form.validate_on_submit(): # sucess passing data
        event = app.db.get_event_info(form.data["search"], search_type=form.data["result"])
        results = [(x[2], x[3], x[5], url_for("event_info", name=x[2], type=x[3], gender=x[5], age_group=x[4], id = x[0])) for x in event]
        flash(results)

    return render_template("event_search.html", form=form)


@app.route("/add_student", methods = ["GET","POST"])
def add_student():


    class a1(forms.AddStudentForm):
        class_ = StringField("Class", validators=[InputRequired()])
    class a2(forms.AddStudentForm):
        house = StringField("House", validators=[InputRequired()])
    class a3(forms.AddStudentForm):
        class_ = StringField("Class", validators=[InputRequired()])
        house = StringField("House", validators=[InputRequired()])

    if request.args.get("class_","None") == "1" and request.args.get("house","None") == "1":
        form = a3()

    elif request.args.get("class_","None") == "1":
        form = a1()
    elif request.args.get("house", "None") == "1":
        form = a2()
    else:
        form = forms.AddStudentForm()

    if form.validate_on_submit(): # sucess passing data
        app.db.add_participant([form.data.get("name_last"),form.data.get("name_first"),form.data.get("gender"),78,form.data.get("house"),str(form.data.get("dob")), form.data.get("stu_id")]) # TODO: fix year
        flash(("s", "Success Adding: %s %s"%(form.data.get("name_first"), form.data.get("name_last")))) # TODO: db stuff

    return render_template("input_template.html", form=form)


@app.route("/edit_student", methods = ["GET","POST"])
def edit_student():
    if request.args.get("id", "None") == "None":
        return redirect("/add_student") # no use for that id send to create page
    try:
        user = app.db.get_participant_info(request.args.get("id"), "db_id")[0]
    except IndexError:
        return redirect("/add_student") # no use for that id send to create page


    a = {"name_first":user[2], "name_last":user[1], "clas":user[4], "gender":user[3], "house":user[5], "dob":user[6], "stu_id":user[7]}
    b = {k: v for k, v in request.form.items() if v is not ""}
    a.update(b) # use new form data to override default

    form = forms.AddStudentForm(ImmutableMultiDict(a))

    if form.validate_on_submit(): # sucess passing data
        app.db.update_participant([form.data.get("name_last"),form.data.get("name_first"),form.data.get("gender"),78,form.data.get("house"),str(form.data.get("dob")), form.data.get("stu_id")], request.args.get("id")) # TODO: fix year
        flash(("s", "Success editing: %s %s"%(form.data.get("name_first"),form.data.get("name_last")))) # TODO: db stuff

    return render_template("input_template.html", form=form)



@app.route("/add_event", methods = ["GET","POST"])
def add_event():
    form = forms.AddEvent()

    if form.validate_on_submit(): # sucess passing data
        app.db.add_event(["time", form.data.get("name"),form.data.get("age_group"),form.data.get("event_type"),form.data.get("gender")])
        # TODO: rename track_field to age_group, rename timed_score_distance to event_type in db_interact.py
        flash(("s", "Success Adding: %s"%form.data.get("name"))) # TODO: db stuff


    return render_template("input_template.html", form=form)


@app.route("/edit_event", methods = ["GET","POST"])
def edit_event():
    if request.args.get("id", "None") == "None":
        return redirect("/add_event") # no use for that id send to create page
    try:
        event = app.db.get_event_info(request.args.get("id"), "id")[0]

    except IndexError:
        return redirect("/add_event") # no use for that id send to create page


    a = {"name":event[2], "gender":event[5], "age_group":0, "event_type":event[3]} # TODO: age_group
    b = {k: v for k, v in request.form.items() if v is not ""}
    a.update(b) # use new form data to override default

    form = forms.AddEvent(ImmutableMultiDict(a))

    if form.validate_on_submit(): # sucess passing data
        flash(("s", "Success editing: %s %s"%(user[2],user[1]))) # TODO: db stuff

    return render_template("input_template.html", form=form)



@app.route("/user_info")
def user_info():
    return render_template("user_info.html")

@app.route("/event_info", methods=["GET","POST"])
def event_info():
    class AddResults(FlaskForm):
        if request.args.get("age_group","None") == "None":
            name = SelectField("Class", choices=[], validators=[InputRequired()])
        else:
            idiots = [("id_%s"%x[0], "%s %s %s %s"%(x[1],x[2], x[3], x[6])) for x in app.db.get_participant_info(request.args.get("age_group","None"), "year")]
            name = SelectField("Class", choices=idiots, validators=[InputRequired()])
        result = StringField("Result")
        submit = SubmitField("Add")

    form = AddResults()
    if form.validate_on_submit(): # sucess passing data
        app.db.insert_into_results((form.data["name"].split("_")[1], request.args.get("id", "None"), form.data["result"]))

    return render_template("event_info.html", form=form)

@app.route("/download")
def download():
    return render_template("download_template.html", name="fancy name", data=[("Zip","/hello"),("Zip","/hello"),("Zip","/hello"),("Zip","/hello")])

@app.route("/results")
def results():
    return render_template("results.html", data=[("dave", "10000"), ("dave", "10000"), ("dave", "10000"), ("dave", "10000"), ("dave", "10000"), ], event_name="100m sprint", gender="attack helicopter", year="10")

@app.route("/events")
def events():
    return render_template("results.html", data=[(x[0], x[2], x[5], x[3], url_for("event_info", name=x[2], type=x[3], gender=x[5], age_group=x[4], id = x[0])) for x in app.db.get_events()])


@app.context_processor
def utility_processor():
    def get_event_stats(id):
        out = []

        if id == None:
            return out

        for i in app.db.get_results_from_event(id):
            user = app.db.get_participant_info(i[1], "db_id")[0]
            out.append(("%s %s"%(user[2], user[1]), user[4], user[6].split(" ")[0], i[3], url_for("user_info", name_first=user[2], name_last=user[1], house=user[5], gender=user[3], year=user[4], dob=user[6])))

        try:
            out.sort(key = lambda x: x[3], reverse=True)
        except TypeError:
            out.sort(key = lambda x: len(str(x[3])), reverse=True)

        return out
    return dict(get_event_stats=get_event_stats)

@app.context_processor
def utility_processor():
    def get_user_stats(id):
        out = []

        if id == None:
            return out

        return out
    return dict(get_user_stats=get_user_stats)

if __name__ == "__main__":
    app.run(debug = True, use_reloader=True)
