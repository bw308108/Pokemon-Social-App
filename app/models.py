from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin 
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

Team = db.Table(
    'Team',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullible=False),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullible=False)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = generate_password_hash(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String(), nullable=False)
    caption = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)


    def __init__(self, title, img_url, caption, user_id):
        self.title = title 
        self.img_url = img_url
        self.caption = caption
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()