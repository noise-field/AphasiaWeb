# -*- coding: utf-8 -*-

try:
    from os import getuid

except ImportError:
    def getuid():
        return 4000

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/hello/<xname>")
def welcomer(xname):
    return render_template("template.tpl", xname=xname)

@app.route("/temple/")
def index():
    return render_template("index.tpl")

@app.route("/temple/hello")
def hello_templatized():
    return render_template("hello.tpl")

if __name__ == "__main__":
    app.run(port=getuid() + 1000, debug=True)
