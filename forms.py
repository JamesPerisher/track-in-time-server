from flask_wtf import FlaskForm
import wtforms
from wtforms.fields import Field
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, HiddenField
from wtforms.validators import InputRequired
from wtforms.fields.html5 import DateField


class Form(FlaskForm):
    submit = SubmitField("Submit")

    def __init__(self):
        super().__init__()
        self.elements = []
        for i in self.__dict__:
            if isinstance(self.__dict__[i], Field) and not isinstance(self.__dict__[i], SubmitField) and not isinstance(self.__dict__[i], HiddenField):
                self.elements.append(self.__dict__[i])

        # self.elements = enumerate(self.elements)

        return None

class AddStudentForm(Form):
    name_first = StringField("First Name", validators=[InputRequired()])
    name_last = StringField("Last Name", validators=[InputRequired()])
    gender = SelectField("Gender", choices=[("male","Male"), ("female","Female"), ("other","Other"), ("attack","Attack Helicopter")])
    house = SelectField("House", choices=[{"earth":"Earth", "fire":"Fire"}]) # TODO: get from database
    dob = DateField("Date of Birth")

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
