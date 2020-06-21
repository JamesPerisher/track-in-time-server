from flask import render_template, jsonify, request, session, redirect
from dataclasses import User, House, Gender, Event
from forms import *



def add_house():
    form = AddHouseForm(request.form)
    if request.method == 'POST' and form.validate():
        house = House(name=form.name.data)
        recordPages.db.session.add(house)
        recordPages.db.session.commit()

        return redirect('/')

    return render_template("add_house.html", form=form, form_fields=[form.name])


def add_gender():
    form = AddGenderForm(request.form)
    if request.method == 'POST' and form.validate():
        gender = Gender(name=form.name.data)
        recordPages.db.session.add(gender)
        recordPages.db.session.commit()

        return redirect('/')

    return render_template("add_house.html", form=form, form_fields=[form.name])


def add_user():
    form = AddUserForm(request.form)
    form["house"].choices = [(x.id, x.name) for x in House.query.all()]
    if len(form["house"].choices) == 0: pass # we have no houses error
    form["gender"].choices = [(x.id, x.name) for x in Gender.query.all()]
    if len(form["gender"].choices) == 0: pass # we have no genders error

    if request.method == 'POST' and form.validate():
        user = User(name_first=form.name_first.data, name_last=form.name_last.data, dob=form.dob.data, house=form.house.data, gender=form.gender.data)

        recordPages.db.session.add(user)
        recordPages.db.session.commit()

        return redirect('/')

    return render_template("add_user.html", form=form, form_fields=[form.name_first, form.name_last, form.dob, form.house, form.gender])


def add_event():
    form = AddEventForm(request.form)
    form["gender"].choices = [(x.id, x.name) for x in Gender.query.all()]
    if len(form["gender"].choices) == 0: pass # we have no genders error
    if request.method == 'POST' and form.validate():
        event = Event(name=form.name.data, date_from=form.date_from.data, date_to=form.date_to.data, gender=form.gender.data, method=form.method.data)

        recordPages.db.session.add(event)
        recordPages.db.session.commit()

        return redirect('/')

    return render_template("add_event.html", form=form, form_fields=[form.name, form.date_from, form.date_to, form.gender, form.method])


def add_events():
    form = AddEventsForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect('/')

    return render_template("add_event.html", form=form, form_fields=[])
