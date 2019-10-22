# Team HotCocao
# Joseph Yusufov, Hilary Zen, Alice Ni, Devin Lin
# 2019-10-22

import sqlite3  # enable control of an sqlite database
import csv  # facilitate CSV I/O

DB_FILE = "wiki.db"

db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
c = db.cursor()  # facilitate db ops


# < < < INSERT YOUR POPULATE-THE-DB CODE HERE > > >
insert_one = "INSERT INTO users(user_id, username, password) VALUES( 1, \"kingthomas13\", \"Lebron23\")"

#==========================================================

# test SQL stmt in sqlite3 shell, save as string
create_table_users = "CREATE TABLE users(user_id INTEGER PRIMARY KEY, usernamne TEXT, password TEXT, date_created DATETIME DEFAULT current_timestamp);"
c.execute(create_table_users)
#==========================================================

db.commit()  # save changes
db.close()  # close database
