from flask import Flask
from flask import render_template, redirect
from flask import request
import json
import time
import pytz
import numpy as np
import os
import db_interact as db
import datetime


app = Flask(__name__, template_folder='templates')


class form():
    def call(self):
        if self.request.args.to_dict() == {}:
            return render_template(self.form, fields=self.empty)

        base = self.empty.copy()
        res_data = self.request.args.to_dict()
        # makse sure all keys in self.empty are included in base
        base.update(res_data)

        print("Data: %s" % base)

        if "" in [base[x] for x in base]:
            return render_template(self.form, error=("All fields must be filled." if self.error == None else self.error), fields=base)
        self.success = self.event(base)  # calls event funtion
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


@app.route('/add_student')
def add_person():
    empty = {"name_first": "", "name_last": "", "gender": "", "year": "",
             "house": "", "dob": "", "teacher": "", "student_id": ""}
    f = form(request, empty, "add_student_form.html")
    return f.call()


@app.route('/add_teacher')
def add_teacher():
    empty = {"name_first": "", "name_last": "", "gender": "", "year_groups": "",
             "house": "", "dob": ""}
    f = form(request, empty, "add_teacher_form.html")
    return f.call()


@app.route('/add_event')
def add_event():
    empty = {"name": "", "time": "", "age_group": "",
             "track_feild": "", "timed_score_distance": "", "gender": ""}
    f = form(request, empty, "add_event_form.html", event=lambda x: x)
    return f.call()


@app.route('/cmd')
def cmd():
    try:
        a = eval(request.args.to_dict()["cmd"])
        return {"r": a}
    except Exception as e:
        return e


c = db.connection()
c.data_entry()
print("test")
test = c.get_dates()
print(test)
test2 = []
test3 = []
for i in test:
    test2.append(i[0].split("-")[0])
for i in test2:
    if i not in test3:
        test3.append(i)
    else:
        pass
test3.sort(reverse=True)
print(test3)
for i in test3:
    print(i)
    c.add_age_group({"start": ("%s-1-1") %
                     i, "name": ("Year %s %s") % (str((int(datetime.datetime.now().year) - int(i)) - 6), i), "end": ("%s-1-1") % str(int(i) + 1)})

print("test2")
thing = c.get_age_groups()
for i in thing:
    print(i[1], datetime.datetime.fromtimestamp(
        i[2]), datetime.datetime.fromtimestamp(i[3]))
# print(c.get_name_info("Person"))


if __name__ == '__main__':
    app.run()
