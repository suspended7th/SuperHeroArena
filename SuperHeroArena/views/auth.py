from datetime import datetime
from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_nav.elements import View, Subgroup

from ..models.user import User
from ..dbconfig import get_db

bp = Blueprint('auth', __name__)

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = False if 'remember' not in request.form else True
        user = User.query.filter(User.username==username).first()
        if not user:
            flash('User does not exist.  Please Create one.')
        elif user.authenticate(password):
            flash('Successful login')
            login_user(user, remember=remember)
            return redirect('/profile/')
        else:
            flash('Unauthenticated')
    return render_template('login.html')

@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    db = get_db()
    if request.method == 'POST':
        print(request.form, flush=True)
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        remember = False if 'remember' not in request.form else True
        error = None
        if not username:
            error = 'Username is required'
            flash(error)
        if not password:
            error = 'Password is required'
            flash(error)
        if not email:
            error = 'Email is required'
            flash(error)
        if not error:
            user = User(username=username, password=password, email=email)
            try:
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=remember)
                flash('user created')
                return redirect('/profile/')
            except:
                flash('There was an issue adding the user')
            
        return redirect('/signup/')
            
    return render_template('signup.html')

@bp.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/login/')

@bp.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        email = request.form['email']
        try:
            error = ''
            if old_password:
                if current_user.authenticate(old_password):
                    current_user.set_password(new_password)
                else:
                    error = 'Invalid Old Password.  User Not Updated.'
                    flash(error)
            if not error:
                current_user.username = username
                current_user.email = email
                db.session.commit()
        except:
            flash("There was an issue updating the user")

    return render_template('profile.html', user=current_user)

@bp.route('/update_high_score/', methods=['POST'])
def update_high_score():
    db = get_db()
    score = int(request.form['score'])
    hero = request.form['hero']
    if score > current_user.high_score:
        try:
            current_user.high_score = score
            current_user.high_score_hero = hero
            current_user.high_score_date = datetime.utcnow()
            db.session.commit()
        except:
            flash("There was an issue updating the user")
    return redirect('/profile/')

def generate_nav():
    nav = Subgroup(
        'User'
    )
    if current_user.is_authenticated:
        nav.items.append(View('Profile', 'auth.profile'))
        nav.items.append(View('Logout', 'auth.logout'))
    else:
        nav.items.append(View('Login', 'auth.login'))
        nav.items.append(View('Sign Up', 'auth.signup'))
    return nav
