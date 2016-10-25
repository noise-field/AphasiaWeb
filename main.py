import taskGenerator
from flask import Flask, request, render_template

try:
    from os import getuid
except ImportError:
    def getuid():
        return 4000

generator = taskGenerator.TaskGenerator('subjects.txt', 'tails.txt')

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')
    
from flask import request, json
@app.route('/result', methods=['POST'])
def result():
    new_task = None
    global generator
    while True:
        try:
            new_task = generator.getRandom(300)
            break
        except:
            pass
    print(new_task)
    return json.dumps(new_task)

@app.route('/topic', methods=['GET'])
def topic():
    global generator
    #print(request.args['topic_name'])
    topic_name = request.args['topic_name']
    generator.changeTopic(topic_name)
    return 'OK'

if __name__ == "__main__":
    app.run(port=getuid() + 1000, debug=True)