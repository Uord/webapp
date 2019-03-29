from flask import Flask
from flask import request, redirect, session, Response, url_for, render_template, jsonify
import json
from functools import wraps
app = Flask(__name__)
app.counter = 0




@app.route('/')
def start():
        return 'Hello, World!'




@app.route('/login', methods = ['GET','POST'])
def login():
        auth = request.authorization
        username = auth.username
        password = auth.password
        if username == 'TRAIN' and password == 'TuN3L':
                session['username'] = request.authorization.username
                return redirect("https://apkalevelup.herokuapp.com/hello")
        else:
                return  redirect("https://apkalevelup.herokuapp.com/")


@app.route('/hello')
def hello():
        return 'Hello, World!'



@app.route('/method', methods = ['GET', 'POST', 'PUT', 'DELETE'] )
def method():
        return f'{request.method}'

@app.route('/show_data', methods = ['POST'])
def show_data():
        data = request.get_json()
        return json.dumps(data).encode('utf8')

@app.route('/pretty_print_name', methods = ['POST'])
def print_name():
        data = request.get_json()
        data2 = json.dumps(data).encode('utf8')
        data3 = json.loads(data2)
        return f'Na imię mu {data3["name"]}, a nazwisko jego {data3["surename"]}'


@app.route('/counter')
def counter():
        app.counter += 1
        return str(app.counter)

if __name__ == '__main__':
        app.run(debug=False)
