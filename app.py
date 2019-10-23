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

print(db_functions.check_users("kingthomas13", "Lebron23")) # attempt to call a function in db_functions

@app.route('/')  # Login Page
def index():
    # load the template with the user's session info
    return render_template('landing.html')


# Logout removes the User's session from the dictionary stored on the server, even if the cookie still exists
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged Out Succesfully")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.debug = True
    app.run()
