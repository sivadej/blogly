from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User

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
    users = User.query.all()
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
    return redirect(url_for('show_users'))

@app.route('/users/<int:id>')
def show_user_details(id):
    user = User.query.get_or_404(id)
    return render_template('user_details.html', user=user)

@app.route('/users/<int:id>/edit', methods=['POST'])
def show_edit_form(id):
    user = User.query.get_or_404(id)
    return render_template('edit_user.html', user=user)