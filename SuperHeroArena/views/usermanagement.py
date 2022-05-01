from .. import app, db
from ..models.user import User
from flask import render_template, request, abort, redirect

@app.route('/usermanagement/', methods=['GET', 'POST'])
def usermanagement():
    if request.method == 'POST':
        print(request.form, flush=True)
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/usermanagement/')
        except BaseException as err:
            return "There was an issue adding the user\n\r" + str(err)
    else:
        users = User.query.order_by(User.date_created).all()
        return render_template('usermanagement.html', users=users)
    
@app.route('/usermanagement/<id>/', methods=['GET', 'POST'])
def userupdater(id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(User.id==id).first()
        try:
            user.username = username
            user.password = password
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
            
@app.route('/usermanagement/<id>/delete/', methods=['GET', 'POST'])
def userdeleter(id):
    if request.method == 'POST':
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
        