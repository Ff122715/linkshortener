import sqlite3

# подключение и соединение с базой данных
connect = sqlite3.connect('database.db', check_same_thread=False)
cursor = connect.cursor()


# создание таблиц

cursor.execute('''CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"login"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);''')
connect.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS "links" (
	"id"	INTEGER NOT NULL,
	"link"	TEXT NOT NULL UNIQUE,
	"short_link"	TEXT NOT NULL,
	"access"	INTEGER NOT NULL,
	"redirect_count"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);''')
connect.commit()
