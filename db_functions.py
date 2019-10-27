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


def get_user_stories(user_id):
    DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    get_stories = "SELECT story_id FROM edits WHERE user_id = %s;" % user_id
    stories_edited_tuple = list(c.execute(get_stories))
    toreturn = []
    for member in stories_edited_tuple:
        story_id = member[0]
        story_info = c.execute("SELECT * FROM stories WHERE stories.story_id = %s" % (story_id)) 
        for entry in story_info:
            toreturn.append(entry)
    
    db.commit()  # save changes
    db.close()  # close database
    return toreturn

def get_other_stories(user_id):
    DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    other_stories_query = """
    SELECT * FROM stories 
    INNER JOIN edits ON edits.story_id = (
        SELECT story_id FROM edits
        WHERE edits.story_id = stories.story_id
        AND edits.user_id <> %s
        ORDER BY edits.timestamp DESC
        LIMIT 1
    )AND edits.user_id <> %s;""" % (user_id, user_id) 
    result_other_stories = list(c.execute(other_stories_query))
    db.commit()  # save changes
    db.close()  # close database
    return result_other_stories

def get_user_by_id(user_id):
    DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    query = "SELECT username FROM users WHERE user_id == \"%s\";" % (user_id)
    response = list(c.execute(query))
    username = response[0][0]
    db.commit()  # save changes
    db.close()  # close database
    return username

def modify_story(story_id, user_id, edit):
    DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops
    
    body_results = list(c.execute("SELECT body FROM stories WHERE story_id = %s" % story_id))
    body = ""
    for b in body_results:
        body = b[0]
    update_stories = """
        UPDATE stories
        SET body = \"%s\" 
        WHERE story_id = %s;
        """ % ((body + " " + edit), story_id)
    c.execute(update_stories)

    update_edits = """
        INSERT INTO edits(story_id, user_id, edit)
        VALUES(%s, %s, \"%s\")
        """ % (story_id, user_id, edit)
    c.execute(update_edits)

    db.commit()  # save changes
    db.close()  # close database

SELECT * FROM stories 
INNER JOIN edits ON 
edits.story_id = (
    SELECT edits.story_id FROM edits, stories
    WHERE edits.story_id = stories.story_id
    AND edits.story_id IS NOT (
        SELECT story_id FROM edits
        WHERE user_id = 3
    )   
    ORDER BY edits.timestamp DESC
    LIMIT 1
);