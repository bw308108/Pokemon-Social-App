from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user
from app.auth.forms import Pokeform, Usercreationform, LoginForm
from app.models import User 
from werkzeug.security import check_password_hash

import requests



auth = Blueprint('auth',__name__, template_folder='auth_templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
     form = LoginForm()
     if request.method == 'POST':
        if form.validate():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    print('Logged In')
                    login_user(user)
                else:
                    print('Invalid Password')
            else:
                print('User does not exist')
     return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET','POST']) #can now accept post request
def signup():
    forms = Usercreationform() #need to instantiate the Usercretaionform because it is a class
    if request.method == 'POST': #if the specific meothod is a post request on this specific route
        if forms.validate(): #validators, from forms.py
            firstname = forms.firstname.data #firstname is equal to the form (or forms) that we are getting back from the post request 
            lastname = forms.lastname.data
            email = forms.email.data
            password = forms.password.data

            print(firstname, lastname, email, password)

            user = User(firstname, lastname, email, password) #created in instance of User class from models page
            #this is where we are going to pass in the user name that we are getting from our user; see above variables

            user.save_to_db()
            return redirect(url_for('auth.login'))

    return render_template('signup.html', forms=forms) #passed in the instance from form to the signup page
    #now we should be able to utilize the attributes that we built from the Usercreationform on Forms.py