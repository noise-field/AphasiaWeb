import semantic_generator
import logging
from flask import Flask, request, render_template, jsonify, json

try:
    from os import getuid
except ImportError:
    def getuid():
        return 4000


app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/semantics')
def semantics():
    return render_template('semantics.html')


@app.route('/grammar')
def grammar():
    return render_template('grammar.html')


@app.route('/semantic_task', methods=['POST'])
def get_semantic_task():
    try:
        generator = semantic_generator.TaskGenerator()
        new_task = generator.get_random(300)
        logging.info(new_task)
        # return json.dumps(new_task)
        return jsonify(**new_task)
    except Exception as e:
        logging.error(str(e))
        return jsonify(**{"task": "Произошла ошибка. Попробуйте обновить страницу",
                          "options": [""] * 4})


@app.route('/topic_grammar', methods=['GET'])
def topic_grammar():
    generator = semantic_generator.TaskGenerator()
    # print(request.args['topic_name'])
    topic_name = request.args['topic_name']
    generator.change_topic(topic_name)
    logging.info("Grammar generation task status: OK")


@app.route('/topic_semantics', methods=['GET'])
def topic_semantics():
    generator = semantic_generator.TaskGenerator()
    topic_name = request.args['topic_name']
    generator.change_topic(topic_name)
    logging.info("Semantic generation task status: OK")
    return ""

if __name__ == "__main__":
    app.run(port=getuid() + 1000, debug=True)