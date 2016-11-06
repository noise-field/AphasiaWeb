import semantic_generator
import grammar_generator
import logging
from flask import Flask, request, render_template, jsonify
import sys

try:
    from os import getuid
except ImportError:
    def getuid():
        return 4000


app = Flask(__name__)
AVAILABLE_TASKS = ["grammar", "semantics"]

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')


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
    app.run(port=getuid() + 1000, debug=True)