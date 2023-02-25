from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from .forms import PostForm, PokeForm
from app.models import Post
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
                    "image": data['sprites']['other']['home']['front_shiny'],
                    "attack_base_stat":data['stats'][1]['base_stat'],
                    "hp_base_stat" :data['stats'][0]['base_stat'],
                    "defense_base_stat": data['stats'][2]['base_stat']
                }
            print(poke_profile)
            print(poke_profile['image'])
    return render_template('pokeform.html', form=form, poke_profile=poke_profile)


@social.route('/posts/<int:post_id>')
def view_single_post(post_id):
    post = Post.query.get(post_id)
    if post:        
        return render_template('single_post.html', post=post)
    else:
        return redirect(url_for('social.view_posts'))

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


