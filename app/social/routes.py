from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from .forms import PostForm, PokeForm
from app.models import Post, Catch
import requests

social = Blueprint('social', __name__, template_folder='social_templates')

@social.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            #need to instantiate Post from Models
            post = Post(title, img_url, caption, current_user.id)

            #add post to our database
            post.save_to_db()
            return redirect(url_for('social.view_posts'))
    return render_template('create_post.html', form=form )

@social.route('/posts')
def view_posts():
    posts = Post.query.all() #posts is equal to Post model, query all posts inside the table, using SQL Alchemy command
    print(posts)
    return render_template('feed.html', posts=posts[::-1])

@social.route('/posts/forms', methods=['GET', 'POST'])
def pokemon():
    form = PokeForm()
    poke_profile = {}
    if request.method == 'POST':
        if form.validate():
            pokemon_name = form.name.data
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}')
            if response.status_code != 200:
                print(f'{pokemon_name} is not a valid pokemon name. Please double check your spelling.')
            else:
                print('it worked')
                data = response.json()
                poke_profile = {
                    "name":data['name'],
                    "base_experience": data['base_experience'],
                    "abilities": data['abilities'][0]['ability']['name'],
                    "image": data['sprites']['other']['home']['front_shiny'],
                    "attack_base_stat":data['stats'][1]['base_stat'],
                    "hp_base_stat" :data['stats'][0]['base_stat'],
                    "defense_base_stat": data['stats'][2]['base_stat']
                }



                # name = poke_profile['name'] #assigning stats to a variable
                # base_experience = poke_profile['base_experience']
                # abilities = poke_profile['abilities']
                # image = poke_profile['image']
                # base_stat = poke_profile['hp_base_stat']
                # attack_base = poke_profile['attack_base_stat']
                # defense_base = poke_profile['defense_base_stat']
       


            # catch = Catch(name, base_experience, abilities, image, base_stat, attack_base, defense_base, current_user.id)
            # catch.save_to_db() 
            # print('{pokemon_name} added to db')

    return render_template('pokeform.html', poke_profile=poke_profile, form=form)


@social.route('/posts/<int:post_id>')
def view_single_post(post_id):
    post = Post.query.get(post_id)
    if post:        
        return render_template('single_post.html', post=post)
    else:
        return redirect(url_for('social.view_posts'))


@social.route('/posts/test')
def pokedex():
    pokemon_name = ''
    ball = poke(pokemon_name)
    return render_template('test.html', ball=ball)

@social.route('/posts/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    form = PostForm()
    post = Post.query.get(post_id)
    if current_user.id == post.user_id:
        if request.method == 'POST':
            if form.validate():
                title = form.title.data
                img_url = form.img_url.data
                caption = form.caption.data

                #update post on database
                post.title = title 
                post.img_url = img_url
                post.caption = caption

                #add post to our database
                post.update_db()

                return redirect(url_for('social.view_posts'))
    else:
        flash('You are not allowed to be here!')
        return redirect(url_for('social.view_posts'))
    return render_template('update_post.html', form=form, post=post )


@social.route('/posts/delete/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        post.delete_from_db()
    return redirect(url_for('social.view_posts'))


