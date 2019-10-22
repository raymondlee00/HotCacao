# Team HotCocao
# Joseph Yusufov, Hilary Zen, Alice Ni, Devin Lin
# 2019-10-22

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import flash
from flask import url_for
import sqlite3  # enable control of an sqlite database
import os

app = Flask(__name__)  # create instance of class Flask
app.secret_key = os.urandom(24)

DB_FILE = "wiki.db"
db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
c = db.cursor()  # facilitate db ops

query = "SELECT * FROM users;"
user_list = c.execute(query)
for member in user_list:
    print(member)


@app.route('/')  # Login Page
def index():
    # load the template with the user's session info
    if session.get("user") == CREDENTIALS.get('user') and session.get("password") == CREDENTIALS.get('password'):
        return redirect('/auth')
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
