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
    # app.remove_webhook()
    # bot.set_webhook(url="https://{}.herokuapp.com/{}".format(app_name, token))
    return "Hello from Heroku!", 200

@app.route('/reg', methods=['POST'])
def register():
    login = str(request.json.get("login", None))
    password = str(request.json.get("password", None))
    functions_db.reg(login, password)
    if functions_db.reg(login, password):
        return make_response('Пользователь зарегистрирован')
    else:
        return make_response('Ошибка при регистрации пользователя')

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
