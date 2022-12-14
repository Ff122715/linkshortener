from database import connect, cursor

#поиск пользователя в базе по логину
def findUser(login):
    return cursor.execute('SELECT * FROM users WHERE login=?', (login,)).fetchone()

def findId(login):
    return cursor.execute('SELECT id FROM users WHERE login=?', (login,)).fetchone()

# регистрация
def reg(login, password):
    if findUser(login) == None:
        cursor.execute('INSERT INTO users(login, password) VALUES (?, ?)', (login, password))
        connect.commit()
        return True

# авторизация
def auth(login, password):
    if findUser(login) == None:
        return 'Пользователь не зарегестрирован'
    else:
        cursor.execute('SELECT password FROM users WHERE password=?', (password,)).fetchone()
        return True
        # passw = cursor.execute('SELECT password FROM users WHERE password=?', (password,)).fetchone()
        # if passw != None:
        #     return 'Вы успешно авторизовались'
        # else:
        #     return 'Неправильный пароль'

def passwd(login):
    if findUser(login) != None:
        return cursor.execute('SELECT password FROM users WHERE login=?', (login,)).fetchone()[0]

# добавление ссылки в базу
def add_link(link, short_link, access, login):
    cursor.execute('INSERT INTO links(link, short_link, access, user_id) VALUES (?, ?, ?, ?)', (link, short_link, access, login))
    connect.commit()

def redirect(short_link):
    cursor = connect.cursor()
    count = int(cursor.execute('SELECT redirect_count FROM links WHERE short_link=?', (short_link,)).fetchone()[0])
    count += 1
    cursor.execute('UPDATE links SET redirect_count=? WHERE short_link=?', (count, short_link,))
    connect.commit()
    return str(count)


# список ссылок пользователя
def userLinksList(login):
    res = cursor.execute('SELECT short_link FROM links WHERE user_id=?', (login,)).fetchall()
    list = ''
    for i in res:
        list += f'{str(i[0])} \n'
    return list


# удаление ссылки
def deleteLink(short_link):
    cursor.execute('DELETE FROM links WHERE short_link=?', (short_link,))
    connect.commit()
    return 'Cсылка удалена'


# добавление (изменение) псевдонима
def changeShortLink(new_short_link, short_link, login):
    cursor.execute('UPDATE links SET short_link=? WHERE user_id=? AND short_link=?', (new_short_link, login, short_link))
    connect.commit()


# поиск логина по короткой ссылке
def searchUserOnLink(short_link):
    return cursor.execute('SELECT user_id FROM links WHERE short_link=?', (short_link,)).fetchone()[0]


def findAccessLink(short_link):
    return cursor.execute('SELECT access FROM links WHERE short_link=?', (short_link,)).fetchone()[0]


def changeAccess(short_link, user, access):
    owner = searchUserOnLink(short_link)
    old_access = findAccessLink(short_link)
    if user == owner and int(access) != old_access:
        cursor.execute('UPDATE links SET access=? WHERE user_id=? AND short_link=?', (int(access), user, short_link))
        connect.commit()
        return 'Доступ изменен'
    elif int(access) == old_access:
        return 'Это текущий доступ ссылки'
    return 'Вы не можете изменить доступ'