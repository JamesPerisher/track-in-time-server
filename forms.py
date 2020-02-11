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
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, HiddenField, RadioField, SelectMultipleField
from wtforms import widgets
from wtforms.validators import InputRequired, Length, EqualTo
from wtforms.fields.html5 import DateField
import db_interact as custom_db

app = custom_db.connection()
app.start() # start db thread to get inital config data


# constants
GENDER = SelectField("Gender", choices=[("male","Male"), ("female","Female"), ("other","Other")])
CLASS_ = SelectField("Class", choices=[("%s"%x[0],"%s"%x[0]) for x in app.get_data_types("year")] + [("new","New")]) if (len([("%s"%x[0],"%s"%x[0]) for x in app.get_data_types("year")]) != 0) else StringField("Class", validators=[InputRequired()])
HOUSE = SelectField("House", choices=[("%s"%x[0],"%s"%x[0]) for x in app.get_data_types("house")] + [("new","New")]) if (len([("%s"%x[0],"%s"%x[0]) for x in app.get_data_types("house")]) != 0) else StringField("House", validators=[InputRequired()])
DOB = DateField("Date of Birth", validators=[InputRequired()])


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """

    widget = widgets.ListWidget(prefix_label=True)
    option_widget = widgets.CheckboxInput()


class Form(FlaskForm):
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.elements = []
        for i in self.__dict__:
            el = self.__dict__[i]
            if isinstance(el, Field) and not isinstance(el, SubmitField) and not isinstance(el, HiddenField) and not isinstance(el, RadioField):

                self.elements.append(el)

        # self.elements = enumerate(self.elements)

        return None

class Login(Form):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class SearchUserForm(Form):
    result = SelectField("Search type", choices=[("name_first","First Name"), ("name_last", "Last Name"), ("year", "Year"), ("house", "House")])
    search = StringField("Search term (user name, event name)", validators=[InputRequired()])

class SearchEventForm(Form):
    result = SelectField("Search type", choices=[("name","Event Name"), ("track_field", "Event Type"), ("gender", "Gender")])
    search = StringField("Search term (user name, event name)", validators=[InputRequired()])


class AddStudentForm(Form):
    name_first = StringField("First Name", validators=[InputRequired()])
    name_last = StringField("Last Name", validators=[InputRequired()])

    class_ = CLASS_
    gender = GENDER
    house = HOUSE
    dob = DOB

    stu_id = StringField("Student id")


class AddEvent(Form):
    name = StringField("Event Name", validators=[InputRequired()])
    gender = MultiCheckboxField('Gender', choices=[("male","Male"), ("female","Female"), ("other","Other")])
    years = MultiCheckboxField('Years', choices=[(str(x), "Year %s"%x) for x in [5,6,7,8,9,10,11,12,"other"]])
    event_type = SelectField("Event type", choices=[("timed","Timed"), ("distance","Distance"), ("placed","Placed"), ])


class EditEvent(Form):
    name = StringField("Event Name", validators=[InputRequired()])
    gender = GENDER
    age_group = SelectField("AgeGroup", choices=[("%s"%x[0],"%s"%x[0]) for x in app.get_data_types("year")])
    event_type = SelectField("Event type", choices=[("timed","Timed"), ("distance","Distance"), ("placed","Placed"), ])


app.kill() # kill thread to allow main db thread to not have errors
