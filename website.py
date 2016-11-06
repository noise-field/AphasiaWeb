from flask import Flask, jsonify
from flask import render_template
import taskGenerator
import webbrowser
app = Flask(__name__)

generator = taskGenerator.TaskGenerator('subjects.txt', 'tails.txt')
print('Visit localhost:5000/index')
webbrowser.open('http://localhost:5000/index')

@app.route('/')
def hello():
	return("The site is up")

from flask import render_template

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
			new_task = generator.get_random(300)
			break
		except:
			pass
	print(new_task)
	return jsonify(**new_task)

@app.route('/topic', methods=['GET'])
def topic():
	global generator
	#print(request.args['topic_name'])
	topic_name = request.args['topic_name']
	generator.change_topic(topic_name)
	return 'OK'

if __name__ == "__main__":
	app.run()