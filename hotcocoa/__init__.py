# Team HotCocao
# Joseph Yusufov, Hilary Zen, Alice Ni, Devin Lin
# 2019-10-28

# DATABASE IS CREATED WITH "db_builder.py"
# DATABASE IS INTERACTED WITH USING FUNCTIONS IN "db_functions.py in utl"

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import flash
from flask import url_for
from utl import db_functions
import sqlite3  # enable control of an sqlite database
import os

DIR = os.path.dirname(__file__) or '.'
DIR += '/'

app = Flask(__name__)  # create instance of class Flask
print("Running my app.py={}.".format(__name__))    # ADDED THIS LINE
print("My app={}.".format(app))                      # ADDED THIS LINE
app.secret_key = os.urandom(24)
database = db_functions # create instance of database interaction apparatus
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
        if database.checkfor_credentials(request.args.get('username'), request.args.get('password')):
            session['user'] = request.args.get('username')
            session['password'] = request.args.get('password')
            session['id'] = database.get_user_id(request.args.get('username'))
            session['date_created'] = database.get_user_date(request.args.get('username'))
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
        if database.checkfor_username(request.args.get('username')):
            flash('Account with that username already exists')
            return redirect(url_for('register'))
        else:
            database.create_user(request.args.get('username'), request.args.get('password'))
            flash('Account Created')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/create')
def create():
    if not 'user' in session:
        flash('Not Logged in')
        return redirect(url_for('index'))
    elif request.args:
        database.create_story(session['id'], request.args.get('title'), request.args.get('text'))
        flash('Created Story')
        return redirect(url_for('dashboard'))
    return render_template("create_story.html")

@app.route('/modify')
def modify():
    if not 'user' in session:
        flash('Not Logged In')
        return redirect(url_for('index'))
    elif request.args:
        database.modify_story(request.args.get('story_id'), session['id'][0][0], request.args.get('edit'))
        flash('Added to Story')
        return redirect(url_for('dashboard'))
    print(database.get_other_stories(session['id'][0][0]))
    return render_template('modify.html', stories = database.get_other_stories(session['id'][0][0]))


@app.route('/dashboard')
def dashboard():
    if not 'user' in session:
        flash('Not Logged in')
        return redirect(url_for('index'))
    return render_template('welcome.html', username = session['user'], id = session['id'][0][0], date_created = session['date_created'][0][0], stories = database.get_user_stories(session['id'][0][0]))


# Logout removes the User's session from the dictionary stored on the server, even if the cookie still exists
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged Out Succesfully")
    return redirect(url_for("index"))

print("Running my app.py={}.".format(__name__))    # ADDED THIS LINE
print("My app={}.".format(app))                      # ADDED THIS LINE

if __name__ == "__main__":
    app.debug = False
    app.run()
