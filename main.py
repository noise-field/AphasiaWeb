import semantic_generator
import grammar_generator
import logging
from flask import Flask, request, render_template, jsonify, make_response, redirect
import sys
import sqlite3
import os
from hashlib import md5

try:
    from os import getuid
except ImportError:
    def getuid():
        return 4000


app = Flask(__name__)
AVAILABLE_TASKS = ["grammar", "semantics"]
PATIENTDB_PATH = "patientdb.db"


@app.route('/')
def hello():
    try:
        email = request.cookies['email']
        password = request.cookies['password']
        conn = sqlite3.connect(PATIENTDB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE email = ? AND password = ?", [email, password])
        res = cursor.fetchone()
        if res:
            return render_template('index.html', logged_in=True, name=res[1])
        else:
            return render_template('index.html', logged_in=False)
    except KeyError:
        return render_template('index.html', logged_in=False)


@app.route('/index')
def index():
    return redirect("/")


@app.route('/logout')
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie('email', '', expires=0)
    resp.set_cookie('password', '', expires=0)
    return resp

@app.route('/semantics')
def semantics():
    return render_template('semantics.html', kind="semantic")


@app.route('/grammar')
def grammar():
    return render_template('grammar.html', kind="grammar")

# @app.route('/grammar')
# @app.route('/semantics')
# def tasks():
#     path = request.path.strip("/")
#     if path in AVAILABLE_TASKS:
#         if path == "grammar":
#             kind = "grammar"
#         if path == "semantics":
#             kind = "semantic"
#         else:
#             return render_template('index.html')
#         return render_template('task.html', kind=kind)
#     else:
#         return render_template('index.html')


@app.route('/semantic_task', methods=['POST'])
def get_semantic_task():
    try:
        generator = semantic_generator.TaskGenerator()
        generator.change_topic(request.form['topic'])
        new_task = generator.get_random(300)
        logging.info(new_task)
        # return json.dumps(new_task)
        return jsonify(**new_task)
    except Exception as e:
        logging.error(str(e))
        return jsonify(**{"task": "Произошла ошибка. Попробуйте обновить страницу",
                          "options": [""] * 4})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        try:
            email = request.cookies['email']
            password = request.cookies['password']
            conn = sqlite3.connect(PATIENTDB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE email = ? AND password = ?", [email, password])
            res = cursor.fetchone()
            if res:
                return render_template('index.html', logged_in=True, name=res[1])
            else:
                return render_template('registrationpage.html')
        except KeyError:
            return render_template('registrationpage.html')
    elif request.method == "POST":
        try:
            email = request.form['email']
            assert len(email) > 5, "Неверный формат почтового адреса"
            password = request.form['password']
            password_repeat = request.form['password_repeat']
            assert password == password_repeat, "Пароли не совпадают"
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['last_name']
            conn = sqlite3.connect(PATIENTDB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE email = ?", [email])
            res = cursor.fetchone()
            if res:
                return render_template('registrationpage.html', error="Пользователь с такой почтой уже зарегистрирован")
            else:
                query = "INSERT INTO patients (first_name, middle_name, last_name, email, password) VALUES (?, ?, ?, ?, ?)"
                hash = md5()
                hash.update(password.encode())
                password = hash.hexdigest()
                cursor.execute(query, [first_name, middle_name, last_name, email, password])
                conn.commit()
                conn.close()
                return render_template("/loginpage.html", message="Регистрация успешна", error=False)
        except KeyError:
            return render_template('registrationpage.html', error="Не все поля заполнены.")
        except AssertionError as e:
            render_template('registrationpage.html', error=str(e))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("loginpage.html")
    else:
        email = request.form.get('email')
        logging.info("Logging in user: {}".format(email))
        password = request.form.get('password')
        try:
            logging.info(request.form)
            conn = sqlite3.connect(PATIENTDB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT `password` FROM patients WHERE email=?", [email])
            res = cursor.fetchone()
            logging.info(res)
            if res:
                logging.info("User found")
                passhash = md5()
                passhash.update(password.encode())
                digest = passhash.hexdigest()
                if res[0] == digest:
                    logging.debug("Login successful")
                    resp = make_response(redirect("/"))
                    resp.set_cookie("email", email)
                    resp.set_cookie("password", digest)
                    return resp
                else:
                    return render_template("loginpage.html", error=True)
            else:
                return render_template("loginpage.html", error=True)
        except Exception as e:
            logging.exception(str(e))
        return render_template("index.html")


@app.route('/grammar_task', methods=['POST'])
def get_grammar_task():
    try:
        topic = request.form['topic']
        logging.info("Grammar category task query:" + topic)
        generator = grammar_generator.TaskGenerator()
        new_task = generator.get_task(request.form['topic'])
        # logging.info(new_task)
        # return json.dumps(new_task)
        return jsonify(**new_task)
    except Exception as e:
        logging.error(str(sys.exc_info()[-1].tb_lineno) + ": " + str(e))
        return jsonify(**{"task": "Произошла ошибка. Попробуйте обновить страницу",
                          "options": [""] * 4})


# @app.route('/topic_grammar', methods=['GET'])
# def topic_grammar():
#     generator = grammar_generator.TaskGenerator()
#     # # print(request.args['topic_name'])
#     # topic_name = request.args['topic_name']
#     # generator.change_topic(topic_name)
#     # logging.info("Grammar generation task status: OK")
#     return ""


@app.route('/topic_semantics', methods=['GET'])
def topic_semantics():
    generator = semantic_generator.TaskGenerator()
    topic_name = request.args['topic_name']
    generator.change_topic(topic_name)
    logging.info("Semantic generation task status: OK")
    return ""


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(os.getcwd())
    if not os.path.exists(PATIENTDB_PATH):
        logging.info("Creating a new db file.")
        conn = sqlite3.connect(PATIENTDB_PATH)
        cursor = conn.cursor()
        with open("dbscheme.sql") as f:
            cursor.executescript(f.read())
        conn.commit()
        conn.close()
    app.run(port=getuid() + 1000, debug=True)
