import sqlite3

connection = sqlite3.connect('data.db')
curosor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
curosor.execute(create_table)

user = (1, 'user1', '123')
insert_query = "INSERT INTO users VALUES(?,?,?)"

curosor.execute(insert_query,  user)
connection.commit()
connection.close()
