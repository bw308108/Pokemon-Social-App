from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SearchField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    img_url = StringField('Image Url', validators=[DataRequired()])
    caption = StringField('Caption', validators=[DataRequired()]) 
    submit = SubmitField()

class PokeForm(FlaskForm):
    name = StringField('Title', validators=[DataRequired()])
    submit = SubmitField()
    add = SubmitField()