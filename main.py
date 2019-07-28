from flask import Flask
from flask import render_template, redirect
from flask import request
import json
import time
import pytz
import numpy as np
import os
import db_interact as db

app = Flask(__name__, template_folder='templates')


class form():
    def call(self):
        if self.request.args.to_dict() == {}:
            return render_template(self.form, fields=self.empty)

        base = self.empty.copy()
        res_data = self.request.args.to_dict()
        base.update(res_data)  # makse sure all keys in self.empty are included in base

        if "" in [base[x] for x in base]:
            return render_template(self.form, error=("All fields must be filled." if self.error == None else self.error), fields=base)
        self.success = self.event(base) # calls event funtion
        print("Data: %s"%base)
        return render_template(self.form, success=("Success" if self.success == None else self.success), fields=self.empty)

    def __init__(self, request, empty, form, event=lambda x: "data processed but no event has been added", error=None, success=None):
        self.request = request
        self.empty = empty
        self.form = form
        self.event = event
        self.error = error
        self.success = success



@app.route("/")
def home():
    return render_template("home.html")


@app.route('/home')
def home_redirect():
    return redirect("/", code=302)


@app.route('/add_person')
def add_person():
    empty = {"name_first": "", "name_last": "", "gender": "", "year": "",
             "house": "", "dob": "", "teacher": "", "student_id": ""}
    f = form(request, empty, "person_form.html")
    return f.call()

@app.route('/add_event')
def add_event():
    empty = {}
    f = form(request, empty, "event_form.html")
    return f.call()


c = db.connection()
c.data_entry()
print(c.get_name_info("Person"))

if __name__ == '__main__':
    app.run()
