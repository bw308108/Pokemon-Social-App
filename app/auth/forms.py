from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class Pokeform(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField()


class Usercreationform(FlaskForm): #**inherit** from flask form so that we have access to all these methods
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()]) #being imported from wtforms
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) #need equal to module
    submit = SubmitField()

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()