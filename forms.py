from wtforms import Form, StringField, SelectField, DateField, validators

class AddUserForm(Form):
    name_first = StringField('First Name',    [validators.Length(min=0, max=25), validators.DataRequired()])
    name_last  = StringField('Last Name',     [validators.Length(min=0, max=25), validators.DataRequired()])
    dob        = DateField  ('Date of Birth', [validators.DataRequired()], format='%d-%m-%Y')
    house      = SelectField('House',         [validators.DataRequired()], choices=[("ph", "Place Holder")], coerce=int)
    gender     = SelectField('Gender',        [validators.DataRequired()], choices=[("ph", "Place Holder")], coerce=int)

class AddHouseForm(Form):
    name = StringField('House Name',    [validators.Length(min=0, max=25), validators.DataRequired()])

class AddGenderForm(Form):
    name = StringField('Gender Name',    [validators.Length(min=0, max=25), validators.DataRequired()])

class AddEventForm(Form):
    name       = StringField('Event Name',            [validators.Length(min=0, max=50), validators.DataRequired()])
    date_from  = DateField  ('Yongest Date of Birth', [validators.DataRequired()], format='%d-%m-%Y')
    date_to    = DateField  ('Oldest Date of Birth' , [validators.DataRequired()], format='%d-%m-%Y')
    gender     = SelectField('Gender',                [validators.DataRequired()], choices=[(0, "Place Holder")], coerce=int)
    method     = SelectField('Validation method',     [validators.DataRequired()], choices=[("timed", "Timed"), ("placed", "Placed"), ("scored", "Scored")])
