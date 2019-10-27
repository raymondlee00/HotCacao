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
insert_one = "INSERT INTO users(user_id, username, password) VALUES( 1, \"admin\", \"peterstuy\")"
create_table_users = "CREATE TABLE users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, stories_edited TEXT DEFAULT \"\", date_created DATETIME DEFAULT current_timestamp);"
c.execute(create_table_users)
c.execute(insert_one)

insert_story = "INSERT INTO stories(user_id, title, full_text, edit) VALUES( \"admin\", \"hello\", \"The farmer went to the barn and said hello to his animals\", \"The farmer went to the barn and said hello to his animals.\");"
create_table_stories = "CREATE TABLE stories(story_id INTEGER PRIMARY KEY, user_id INTEGER DEFAULT NULL, title TEXT, full_text TEXT, edit TEXT);"
c.execute(create_table_stories)
c.execute(insert_story)

#==========================================================

db.commit()  # save changes
db.close()  # close database
