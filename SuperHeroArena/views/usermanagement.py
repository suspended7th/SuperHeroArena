from ..models.user import User
from flask import render_template, request, abort, redirect, g, Blueprint, flash
from ..dbconfig import get_db

bp = Blueprint('auth', __name__, url_prefix='/usermanagement')

@bp.route('/', methods=['GET', 'POST'])
def usermanagement():
    db = get_db()
    if request.method == 'POST':
        print(request.form, flush=True)
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required'
        if not password:
            error = 'Password is required' if not error else error + '\nPassword is required'
        user = User(username=username, password=password)
        try:
            db.session.add(user)
            db.session.commit()
        except BaseException as err:
            error = "There was an issue adding the user\n" + str(err)
            
        flash(error)
        return redirect('/usermanagement/')
    else:
        users = User.query.order_by(User.date_created).all()
        return render_template('usermanagement.html', users=users)
    
@bp.route('/<id>/', methods=['GET', 'POST'])
def userupdater(id):
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(User.id==id).first()
        try:
            user.username = username
            user.set_password(password)
            db.session.commit()
            return redirect('/usermanagement/{}/'.format(id))
        except:
            return "There was an issue updating the user"
    else:
        user = User.query.filter(User.id==id).first()
        if user:
            return render_template('userupdater.html', user=user)
        else:
            abort(404)
            
@bp.route('/<id>/delete/', methods=['GET', 'POST'])
def userdeleter(id):
    if request.method == 'POST':
        db = get_db()
        user = User.query.filter(User.id==id).first()
        try:
            db.session.delete(user)
            db.session.commit()
            return redirect('/usermanagement/')
        except:
            return "There was an issue updating the user"
    else:
        user = User.query.filter(User.id==id).first()
        if user:
            return render_template('userdeleter.html', user=user)
        else:
            abort(404)

@bp.route('/<id>/login/', methods=['POST'])
def userlogin(id):
    user = User.query.filter(User.id==id).first()
    if user.authenticate(request.form['password']):
        return "Successful login"
    else:
        return "Unauthenticated"
