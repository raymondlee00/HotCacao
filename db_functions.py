import sqlite3  # enable control of an sqlite database

# checkfor_credentials()
# - @return username and password of accounts that meet the credentials in the password (either an empty touple or 1-sized touple)
def checkfor_credentials(username, password):
    DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    query = "SELECT username, password FROM users WHERE users.username = \"%s\" AND users.password = \"%s\";" % (username, password)
    response = list(c.execute(query))
    db.commit()  # save changes
    db.close()  # close database

    return response


def checkfor_username(username):
    DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    query = "SELECT username FROM users WHERE username == \"%s\";" % (username)
    response = list(c.execute(query))
    db.commit()  # save changes
    db.close()  # close database

    return response


def create_user(username, password):
    DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    query = "INSERT INTO users(username, password) VALUES(\"%s\", \"%s\");" % (username, password)
    response = list(c.execute(query))
    db.commit()  # save changes
    db.close()  # close database

    return response


def get_user_id(username):
    DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    query = "SELECT user_id FROM users WHERE username == \"%s\";" % (username)
    response = list(c.execute(query))
    db.commit()  # save changes
    db.close()  # close database
    return response


def get_user_date(username):
    DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    query = "SELECT date_created FROM users WHERE username == \"%s\";" % (username)
    response = list(c.execute(query))
    db.commit()  # save changes
    db.close()  # close database
    return response

def create_story(user_id, title, text):
    DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    print(user_id)
    print(user_id[0])
    print(user_id[0][0])
    query = "INSERT INTO stories( author_id, title, body) VALUES(%s, \"%s\", \"%s\");" % ((str)(user_id[0][0]), title, text)
    c.execute(query)

    retrieve_last_id = "SELECT story_id FROM stories ORDER BY story_id DESC LIMIT 1;"
    last_story_id_tuple = c.execute(retrieve_last_id)
    last_story_id = ""
    for member in last_story_id_tuple:
        last_story_id = member[0]
        # last_story_id += 1
    
    query = "INSERT INTO edits(story_id, user_id, edit) VALUES(%s, %s, \"%s\");" % (last_story_id, user_id[0][0], text) 
    c.execute(query)

    db.commit()
    db.close()


def modify_story(story_id, user_id, edit):
    return