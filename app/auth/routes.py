from flask import Blueprint, redirect, render_template, request, url_for

from app.auth.forms import Pokeform, Usercreationform
from app.models import User

import requests



auth = Blueprint('auth',__name__, template_folder='auth_templates')

@auth.route('/login')
def login():
     form = Usercreationform()
     if request.method == 'POST':
        if form.validate():
            email = form.email.data
            password = form.password.data
     return render_template('login.html', form=form)


@auth.route('/pokeform', methods=['GET', 'POST'])
def pokeform():
    form = Pokeform()
    poke_profile = {}
    if request.method == 'POST':
        if form.validate():
            pokemon_name = form.name.data
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}')
            if response.status_code != 200:
                print(f'{pokemon_name} is not a valid pokemon name. Please double check your spelling.')
            else:
                data = response.json()
                poke_profile = {
                    "name":data['name'],
                    "base_experience": data['base_experience'],
                    "abilities": data['abilities'][0]['ability']['name'],
                    "image": data['sprites']['front_shiny'],
                    "attack_base_stat":data['stats'][1]['base_stat'],
                    "hp_base_stat" :data['stats'][0]['base_stat'],
                    "defense_base_stat": data['stats'][2]['base_stat']
                }
            print(poke_profile)
            print(poke_profile['image'])
    return render_template('pokeform.html', form=form, poke_profile=poke_profile)

@auth.route('/signup', methods=['GET','POST'])
def signup():
    forms = Usercreationform()
    if request.method == 'POST':
        if forms.validate():
            firstname = forms.firstname.data
            lastname = forms.lastname.data
            email = forms.email.data
            password = forms.password.data

            print(firstname, lastname, email, password)

            user = User(firstname, lastname, email, password)


            user.save_to_db()
            return redirect(url_for('auth.login'))

    return render_template('signup.html', forms=forms)