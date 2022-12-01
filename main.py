from flask import Flask, request, redirect, jsonify, make_response
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
import sqlite3, uuid, hashlib, random
from werkzeug.security import generate_password_hash, check_password_hash
import functions_db

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)


@app.route('/', methods=["GET"])
def index():
    return "Hello from Heroku!", 200

@app.route('/reg', methods=['POST'])
def register():
    login = str(request.json.get("login", None))
    password = str(request.json.get("password", None))
    password = generate_password_hash(password)
    if functions_db.reg(login, password):
        return make_response('Пользователь зарегистрирован')
    else:
        return make_response('Ошибка при регистрации пользователя')

@app.route('/auth', methods=['POST'])
def auth():
    login = str(request.json.get("login", None))
    password = str(request.json.get("password", None))
    password = check_password_hash(functions_db.passwd(login), password)
    if functions_db.auth(login, password):
        token = create_access_token(identity=login)
        return make_response(f'Пользователь авторизован, {token}')
    else:
        return make_response('Неверный логин или пароль')


@app.route('/add_link', methods=['POST'])
@jwt_required()
def add_link():
    login = str(get_jwt_identity())
    link = str(request.json.get('link', None))
    short_link = str(request.json.get('short_link', None))
    access = 1
    if link != '':
        if short_link == '':
            short_link = hashlib.md5(link.encode()).hexdigest()[:random.randint(8, 12)]
        functions_db.add_link(link, short_link, access, login)
        return make_response('Ссылка успешно сохранена')
    return make_response('error')

# link = "hbgvfcvfc"
@app.route('/<short_link>')
def redirect(short_link):
    return functions_db.redirect(short_link)

@app.route('/list')
@jwt_required()
def linksList():
    login = str(get_jwt_identity())
    return functions_db.userLinksList(login)

@app.route('/del', methods=['POST'])
@jwt_required()
def delete():
    short_link = str(request.json.get('short_link', None))
    return functions_db.deleteLink(short_link)

@app.route('/change', methods=['POST'])
@jwt_required()
def change():
    login = str(get_jwt_identity())
    short_link = str(request.json.get('short_link', None))
    new_short = str(request.json.get('new_short', None))
    if new_short == '':
        new_short = hashlib.md5(short_link.encode()).hexdigest()[:random.randint(8, 12)]
    functions_db.changeShortLink(new_short, short_link, login)
    return ''


if __name__ == '__main__':
    app.run()
