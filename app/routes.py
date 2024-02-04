from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models import User

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        if 'login' in request.form:
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['username'] = username
                return redirect('/user_interface')
            else:
                error = 'Invalid username or password'
        elif 'register' in request.form:
            username = request.form['username']
            password = request.form['password']
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
    return render_template('index.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/user_interface')
def user_interface():
    if 'username' in session:
        return render_template('user_interface.html', username=session['username'])
    else:
        return redirect('/')
