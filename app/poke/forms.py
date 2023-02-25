from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokeForm(FlaskForm):
    Pokemon = StringField('Title', validators=[DataRequired()])
    submit = SubmitField()