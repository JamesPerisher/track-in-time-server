#!/usr/bin/env python

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

from flask_wtf import FlaskForm
import wtforms
from wtforms.fields import Field
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, HiddenField, RadioField
from wtforms.validators import InputRequired
from wtforms.fields.html5 import DateField


class Form(FlaskForm):
    submit = SubmitField("Submit")

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.elements = []
        for i in self.__dict__:
            el = self.__dict__[i]
            if isinstance(el, Field) and not isinstance(el, SubmitField) and not isinstance(el, HiddenField) and not isinstance(el, RadioField):

                self.elements.append(el)

        # self.elements = enumerate(self.elements)

        return None

class SearchUserForm(Form):
    result = SelectField("Search type", choices=[("name_first","First Name"), ("name_last", "Last Name"), ("year", "Year"), ("house", "House")])
    search = StringField("Search term (user name, event name)", validators=[InputRequired()])

class SearchEventForm(Form):
    result = SelectField("Search type", choices=[("name","Event Name"), ("track_field", "Event Type"), ("gender", "Gender")])
    search = StringField("Search term (user name, event name)", validators=[InputRequired()])


class AddStudentForm(Form):
    name_first = StringField("First Name", validators=[InputRequired()])
    name_last = StringField("Last Name", validators=[InputRequired()])
    clas = SelectField("Class", choices=[("n_1","n_1"), ("n_2","n_2"), ("n_3","n_3"), ("n_5","n_5")])
    gender = SelectField("Gender", choices=[("male","Male"), ("female","Female"), ("other","Other"), ("attack","Attack Helicopter")])
    house = SelectField("House", choices=[("earth","Earth"), ("fire","Fire")]) # TODO: get from database
    dob = DateField("Date of Birth", validators=[InputRequired()])

    stu_id = StringField("Student id")


class AddEvent(Form):
    name_first = StringField("Event Name", validators=[InputRequired()])
    gender = SelectField("Gender", choices=[("male","Male"), ("female","Female"), ("other","Other"), ("attack","Attack Helicopter")])
    age_group = SelectField("AgeGroup", choices=[("age1-age2","age1-age2"), ("age2-age3","age2-age3")])
    event_type = SelectField("Event type", choices=[("t","Timed"), ("s","Scored"), ("p","Placed"), ("tp","Timed and Placed"), ("ts","Timed and Scored"), ("sp","Scored and Placed"), ])

class AddAgeGroups(Form):
    name_first = StringField("Name / Associated year group", validators=[InputRequired()])
    start_date = DateField("Age group start date")
    end_date = DateField("Age group start end")
