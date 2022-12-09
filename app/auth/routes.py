from flask import Blueprint, redirect, render_template, request

from app.auth.forms import Pokeform, Usercreationform

import requests

auth = Blueprint('auth',__name__, template_folder='auth_templates')

@auth.route('/login')
def login():
     user = Usercreationform()
     if request.method == 'POST':
        if user.validate():
            email = user.email.data
            password = user.password.data
     return render_template('login.html', user=user)


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
    user = Usercreationform()
    if request.method == 'POST':
        if user.validate():
            firstname = user.firstname.data
            lastname = user.lastname.data
            email = user.email.data
            password = user.password.data
        print(firstname, lastname, email, password)
    return render_template('signup.html', user=user)