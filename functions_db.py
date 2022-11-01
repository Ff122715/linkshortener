from database import connect, cursor


#поиск пользователя в базе по логину
def findUser(login):
    return cursor.execute('SELECT * FROM users WHERE login=?', (login,)).fetchone()

# регистрация
def reg(login, password):
    if findUser(login) == None:
        cursor.execute('INSERT INTO users(login, password) VALUES (?, ?)', (login, password))
        connect.commit()