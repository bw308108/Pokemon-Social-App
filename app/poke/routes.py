from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from .forms import PokeForm
import requests

poke = Blueprint('poke',__name__, template_folder='poke_templates')


@poke.route('/forms', methods=['GET', 'POST'])
@login_required
def poke_forms():
    form = PokeForm()
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