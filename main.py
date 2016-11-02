import taskGenerator
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


@app.route('/result', methods=['POST'])
def result():
    try:
        new_task = None
        generator = taskGenerator.TaskGenerator('subjects.txt', 'tails.txt')
        new_task = generator.getRandom(300)
        print(new_task)
        # return json.dumps(new_task)
        return jsonify(**new_task)
    except Exception as e:
        logging.error(str(e))
        return jsonify(**{"task": "Произошла ошибка. Попробуйте обновить страницу",
                          "options": [""] * 4})


@app.route('/topic', methods=['GET'])
def topic():
    generator = taskGenerator.TaskGenerator('subjects.txt', 'tails.txt')
    # print(request.args['topic_name'])
    topic_name = request.args['topic_name']
    generator.changeTopic(topic_name)
    return 'OK'

if __name__ == "__main__":
    app.run(port=getuid() + 1000, debug=True)