from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SECRET_KEY']='YOUR_SECRET_KEY'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_home():
    return redirect(url_for('show_users'))

@app.route('/users')
def show_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('show_users.html', users=users)

@app.route('/users/new')
def show_create_user_form():
    return render_template('create_user.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        img_url = request.form['img_url'],
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:id>')
def show_user_details(id):
    user = User.query.get_or_404(id)
    posts = Post.query.filter_by(author_id=id)
    return render_template('user_details.html', user=user, posts=posts)

@app.route('/users/<int:id>/edit')
def show_edit_user_form(id):
    user = User.query.get_or_404(id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:id>/edit', methods=['POST'])
def do_edit_user(id):
    user = User.query.get_or_404(id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['img_url']
    db.session.commit()
    return redirect(f'/users/{user.id}')

@app.route('/users/<int:id>/delete', methods=['POST'])
def remove_user(id):
    print('deleting user')
    user_to_delete = User.query.get_or_404(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('show_users'))

@app.route('/users/<int:id>/posts/new')
def show_add_post_form(id):
    user = User.query.get_or_404(id)
    return render_template('create_new_post.html', user=user)

@app.route('/users/<int:id>/posts/new', methods=['POST'])
def create_new_post(id):
    new_post = Post(
        title = request.form['title'],
        content = request.form['content'],
        author_id = id,
    )
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{id}')

@app.route('/posts/<int:id>')
def show_post_detail(id):
    post = Post.query.get_or_404(id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<int:id>/delete', methods=['POST'])
def remove_post(id):
    post_to_delete = Post.query.get_or_404(id)
    return_route = f'/users/{post_to_delete.user.id}'
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(return_route)

@app.route('/posts/<int:id>/edit')
def show_edit_post_form(id):
    post = Post.query.get_or_404(id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:id>/edit', methods=['POST'])
def do_edit_post(id):
    post = Post.query.get_or_404(id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()
    return redirect(f'/posts/{id}')
