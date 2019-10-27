# Team HotCocao
# Joseph Yusufov, Hilary Zen, Alice Ni, Devin Lin
# 2019-10-22

import sqlite3  # enable control of an sqlite database
import csv  # facilitate CSV I/O

DB_FILE = "wiki.db"

db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
c = db.cursor()  # facilitate db ops


# < < < INSERT YOUR POPULATE-THE-DB CODE HERE > > >

#==========================================================

# test SQL stmt in sqlite3 shell, save as string
create_table_users = "CREATE TABLE users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, date_created DATETIME DEFAULT current_timestamp);"
insert_user = "INSERT INTO users(user_id, username, password) VALUES( 1, \"admin\", \"peterstuy\");"
c.execute(create_table_users)
c.execute(insert_user)

create_table_stories = "CREATE TABLE stories(story_id INTEGER PRIMARY KEY AUTOINCREMENT, author_id INTEGER DEFAULT NULL, title TEXT, body TEXT);"
insert_story = "INSERT INTO stories(story_id, author_id, title, body) VALUES( 1, 1, \"hello\", \"The farmer went to the barn and said hello to his animals\");"
c.execute(create_table_stories)
c.execute(insert_story)

create_table_edits = "CREATE TABLE edits(story_id INTEGER, user_id INTEGER, edit TEXT, timestamp DATETIME DEFAULT current_timestamp);"
insert_edit = "INSERT INTO edits(story_id, user_id, edit) VALUES( 1, 1, \"The farmer went to the barn and said hello to his animals\");"
c.execute(create_table_edits)
c.execute(insert_edit)

#==========================================================

db.commit()  # save changes
db.close()  # close database
