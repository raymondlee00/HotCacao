# Team HotCocao
# Joseph Yusufov, Hilary Zen, Alice Ni, Devin Lin
# 2019-10-22

# DATABASE IS CREATED WITH "db_builder.py"
# DATABASE IS INTERACTED WITH USING FUNCTIONS IN "db_functions.py"

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import flash
from flask import url_for
import db_functions
import sqlite3  # enable control of an sqlite database
import os

app = Flask(__name__)  # create instance of class Flask
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    # load the template with the user's session info
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else: return render_template('landing.html')


@app.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    elif request.args:
        if db_functions.checkfor_credentials(request.args.get('username'), request.args.get('password')):
            session['user'] = request.args.get('username')
            session['password'] = request.args.get('password')
            session['id'] = db_functions.get_user_id(request.args.get('username'))
            session['date_created'] = db_functions.get_user_date(request.args.get('username'))
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Credentials')
            return redirect(url_for('login'))
    else: return render_template('login.html')

@app.route('/register')
def register():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    elif request.args:
        if db_functions.checkfor_username(request.args.get('username')):
            flash('Account with that username already exists')
            return redirect(url_for('register'))
        else:
            db_functions.create_user(request.args.get('username'), request.args.get('password'))
            flash('Account Created')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/create')
def create():


# @app.route('/modify')
# def modify():


@app.route('/dashboard')
def dashboard():
    return render_template('welcome.html', username = session['user'], id = session['id'][0][0], date_created = session['date_created'][0][0]) # modifying checkfor_credentials() might be able to get rid of this "[0][0]" nonsense


# Logout removes the User's session from the dictionary stored on the server, even if the cookie still exists
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged Out Succesfully")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.debug = True
    app.run()
