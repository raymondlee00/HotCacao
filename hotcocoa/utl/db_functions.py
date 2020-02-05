# Team HotCocao
# Joseph Yusufov, Hilary Zen, Alice Ni, Devin Lin
# 2019-10-28

# DATABASE IS CREATED WITH "db_builder.py"
# DATABASE IS INTERACTED WITH USING FUNCTIONS IN "db_functions.py in utl"


import sqlite3  # enable control of an sqlite database
import os

DIR = os.path.dirname(__file__) or '.'
DIR += '/../db/'
DB_FILE = DIR + "wiki.db"
print(DB_FILE)
db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
c = db.cursor()  # facilitate db ops

# @param username provided by user
# @param password provided by user
# @return username and password of accounts that meet the credentials in the password (either an empty touple or 1-sized touple)
def checkfor_credentials(username, password):
    # DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    query = "SELECT username, password FROM users WHERE users.username = \"%s\" AND users.password = \"%s\";" % (username, password)
    response = list(c.execute(query))
    db.commit()  # save changes
    db.close()  # close database

    return response # returns null if credentials are wrong, and the correct info if correct


# @param username of a user
# @return null if the username does not exist, or a list containing the username if it does exsit.
def checkfor_username(username):
    # DB_FILE = DIR + "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    query = "SELECT username FROM users WHERE username == \"%s\";" % (username)
    response = list(c.execute(query))
    db.commit()  # save changes
    db.close()  # close database

    return response


# @param username provided by the user
# @param passoword provided by the user
# Creates a new user in the users table with the supplied username and password
def create_user(username, password):
    # DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    query = "INSERT INTO users(username, password) VALUES(\"%s\", \"%s\");" % (username, password)
    response = list(c.execute(query))
    db.commit()  # save changes
    db.close()  # close database


# @param username of a user in the users table
# @return user id associated with that username
def get_user_id(username):
    # DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    query = "SELECT user_id FROM users WHERE username == \"%s\";" % (username)
    response = list(c.execute(query))
    db.commit()  # save changes
    db.close()  # close database
    return response


# @param username of a user in the users table
# @return the date that the user associated with the username provided was created
def get_user_date(username):
    # DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    query = "SELECT date_created FROM users WHERE username == \"%s\";" % (username)
    response = list(c.execute(query))
    db.commit()  # save changes
    db.close()  # close database
    return response


# @param the user id of the user making the story
# @param the title provided by the creator of the story
# @param the initial text of the story being created
# create a story in the stories table with the provided parameters as data
def create_story(user_id, title, text):
    # DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    # update stories table with new story
    query = "INSERT INTO stories( author_id, title, body) VALUES(%s, \"%s\", \"%s\");" % ((str)(user_id[0][0]), title, text)
    c.execute(query)

    #update edits story with initial edit for the new story by copying data from the last story created
    retrieve_last_id = "SELECT story_id FROM stories ORDER BY story_id DESC LIMIT 1;"
    last_story_id_tuple = c.execute(retrieve_last_id)
    last_story_id = ""
    # retrieve story id of the story just created
    for member in last_story_id_tuple:
        last_story_id = member[0]
    # populate the edits table with info on that story, and the initial edit.
    query = "INSERT INTO edits(story_id, user_id, edit) VALUES(%s, %s, \"%s\");" % (last_story_id, user_id[0][0], text)
    c.execute(query)

    db.commit()
    db.close()


# @param user_id of the user for which the function will retrieve stories
# @return a list of stories that the user has contributed to, including the full text of the stories
def get_user_stories(user_id):
    # DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    get_stories = "SELECT story_id FROM edits WHERE user_id = %s;" % user_id
    stories_edited_tuple = list(c.execute(get_stories))
    toreturn = []
    story_id_store = list() # this is used to store story ids to stop display of repeating stories
    for member in stories_edited_tuple:
        if member[0] not in story_id_store:
            story_id = member[0]
            story_info = c.execute("SELECT * FROM stories WHERE stories.story_id = %s" % (story_id))
            for entry in story_info:
                toreturn.append(entry)
        story_id_store.append(member[0])

    db.commit()  # save changes
    db.close()  # close database
    return toreturn


# @param user_id of the user for which the function will retrieve stories
# @return a list of stories that the user HAS NOT EDITED, returning only the last edit and not the full text.
def get_other_stories(user_id):
    # DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    # retrieve the last update associated with each story
    all_stories_query = """
        SELECT stories.title, a.story_id, a.user_id, a.edit, a.timestamp FROM edits a, edits b, stories
        WHERE a.story_id = b.story_id
        AND a.story_id = stories.story_id
        GROUP BY a.story_id;
        """ 
    result_all_stories = list(c.execute(all_stories_query))
    print(result_all_stories)

    # retrieve the story ids that the user has already contributed to
    modified_stories_query = """
        SELECT story_id FROM edits
        WHERE edits.user_id=%s
    """ % user_id
    result_modified_stories = list(c.execute(modified_stories_query))
    # print(result_modified_stories)
    for member in result_modified_stories:
        member = member[0]
    print(result_modified_stories)
    result_modified_stories = list(dict.fromkeys(result_modified_stories))
    print(result_modified_stories)

    # filter all stories and their associated most recent edits, removing stories that
    # the user has already contributed to
    for i in range(len(result_all_stories)-1, -1, -1):
        s_id = result_all_stories[i][1]
        print(s_id)
        for no_good in result_modified_stories:
            print("\t%d" % no_good[0])
            if s_id == no_good[0]:
                result_all_stories.remove(result_all_stories[i])
    db.commit()
    db.close()
    # print(result_all_stories)
    # print("----------")
    return(result_all_stories)


# @param user id of a user in the users table
# @return the username associated with that user id
def get_user_by_id(user_id):
    # DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    query = "SELECT username FROM users WHERE user_id == \"%s\";" % (user_id)
    response = list(c.execute(query))
    username = response[0][0]
    db.commit()  # save changes
    db.close()  # close database
    return username


# @param the story id of the story to be modified
# @param the user modifying the story
# @param the edit that the user is appending to the story
# updates the story in the stories table, and adds a new entry in the edits table
def modify_story(story_id, user_id, edit):
    # DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    # retrieves the current body of the story
    body_results = list(c.execute("SELECT body FROM stories WHERE story_id = %s" % story_id))
    body = ""
    for b in body_results:
        body = b[0]

    # appends edit to the body of the story in the stories table
    update_stories = """
        UPDATE stories
        SET body = \"%s\"
        WHERE story_id = %s;
        """ % ((body + " " + edit), story_id)
    c.execute(update_stories)

    # creates a new entry in the edits table with the provided info
    update_edits = """
        INSERT INTO edits(story_id, user_id, edit)
        VALUES(%s, %s, \"%s\")
        """ % (story_id, user_id, edit)
    c.execute(update_edits)

    db.commit()  # save changes
    db.close()  # close database

db.commit()
db.close()
