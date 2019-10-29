import sqlite3  # enable control of an sqlite database
DB_FILE = "wiki.db"
db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
c = db.cursor()  # facilitate db ops

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

    # print(user_id)
    # print(user_id[0])
    # print(user_id[0][0])
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

def get_other_stories(user_id):
    DB_FILE = "wiki.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops

    all_stories_query = """
        SELECT stories.title, a.story_id, a.user_id, a.edit, a.timestamp FROM edits a, edits b, stories
        WHERE a.story_id = b.story_id
        AND a.story_id = stories.story_id
        GROUP BY a.story_id;
        """ 
    result_all_stories = list(c.execute(all_stories_query))
    print(result_all_stories)

    modified_stories_query = """
        SELECT story_id FROM edits
        WHERE edits.user_id=%s
    """ % user_id
    result_modified_stories = list(c.execute(modified_stories_query))
    print(result_modified_stories)

    for member in result_modified_stories:
        member = member[0]
    print(result_modified_stories)
    result_modified_stories = list(dict.fromkeys(result_modified_stories))
    print(result_modified_stories)

    for i in range(len(result_all_stories)-1, -1, -1):
        s_id = result_all_stories[i][1]
        print(s_id)
        for no_good in result_modified_stories:
            print("\t%d" % no_good[0])
            if s_id == no_good[0]:
                result_all_stories.remove(result_all_stories[i])
    db.commit()
    db.close()
    print(result_all_stories)
    print("----------")
    return(result_all_stories)
    # through testing, the element closest to the end of the list is the most recent edit of the story
    # result_other_stories.reverse()
    # filtered_list = list()
    # story_id_store = list()
    # for entry in result_other_stories:
    #     if entry[5] == user_id: # entry[5] is who edited the story
    #         story_id_store.append(entry[0])
    # for entry in result_other_stories:
    #     #print(entry)
    #     if entry[0] not in story_id_store:
    #         filtered_list.append(entry)
    #         story_id_store.append(entry[0])
    # db.commit()  # save changes
    # db.close()  # close database
    # print(filtered_list)
    # return filtered_list

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


    # SELECT * FROM stories INNER JOIN edits ON edits.story_id = (
    #     SELECT story_id FROM edits
    #     WHERE edits.story_id = stories.story_id
    #     AND edits.story_id NOT IN(
    #         SELECT story_id FROM edits
    #         WHERE edits.user_id = 3
    #     )
    #     ORDER BY edits.timestamp DESC
    #     LIMIT 1
    # )

# SELECT edits.story_id FROM edits, stories
# WHERE edits.story_id = stories.story_id
# AND edits.story_id NOT IN(
#     SELECT story_id FROM edits
#     WHERE edits.user_id=3
# )
# ORDER BY edits.timestamp DESC
# LIMIT 1


# select * from stories inner join(
#     select distinct on(story_id) * from edits
#     order by date_created desc
# ) as most_recent_story_edit
# on stories.story_id = most_recent_story_edit.story_id;

# SELECT * FROM stories INNER JOIN edits ON edits.story_id = (
#     SELECT story_id FROM edits
#     WHERE edits.story_id=stories.story_id
#     AND edits.story_id NOT IN(
#         SELECT story_id FROM edits
#         WHERE edits.user_id=3
#     )
#     ORDER BY edits.timestamp DESC
#     LIMIT 1
# );

# SELECT * FROM stories INNER JOIN edits ON edits.story_id = (
#     SELECT story_id FROM edits
#     WHERE edits.story_id=stories.story_id
#     AND edits.story_id NOT IN(
#         SELECT story_id FROM edits
#         WHERE edits.user_id= 3
#     )
#     ORDER BY edits.timestamp DESC
#     LIMIT 1
# );

# SELECT * FROM stories INNER JOIN (
#     SELECT edits.story_id, edits.user_id, edit, timestamp FROM edits, stories
#     WHERE edits.story_id=stories.story_id
#     ORDER BY edits.timestamp DESC
#     LIMIT 1
# ) as most_recent_edit
# ON most_recent_edit.story_id = stories.story_id

# select * from stories inner join(
#     select * from edits
#     order by story_id, timestamp desc
# ) as most_recent_edit
# on stories.story_id = most_recent_edit.story_id


#    AND edits.story_id NOT IN(
#        SELECT story_id FROM edits
#        WHERE edits.user_id=4
#    )

    # SELECT * FROM stories INNER JOIN edits ON edits.story_id = (
    #     SELECT story_id FROM edits
    #     WHERE edits.story_id=stories.story_id
    #     ORDER BY edits.timestamp DESC
    #     LIMIT 1
    # );

# select * from stories inner join(
#     select * from edits
#     order by story_id, timestamp desc
#     LIMIT 1
# ) as most_recent_edit
# on stories.story_id = most_recent_edit.story_id


# SELECT story_id, title FROM stories LEFT JOIN (
#     SELECT edit, timestamp
#     FROM edits
#     ORDER BY stories.story_id, timestamp
#     LIMIT 1
# ) as recent_edit
# ON stories.story_id = recent_edit.story_id;

# SELECT stories.title, a.story_id, a.user_id, a.edit, a.timestamp FROM edits a, edits b, stories
# WHERE a.story_id = b.story_id
# AND a.story_id = stories.story_id
# GROUP BY a.story_id;
print(get_other_stories(4))

db.commit()
db.close()