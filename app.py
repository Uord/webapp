from flask import Flask
from flask import request, redirect, session, Response, url_for, render_template
import json
from functools import wraps

app = Flask(__name__)
app.counter = 0



@app.route('/')
def hello():
        return 'Hello, World!'


def check_auth(username, password):
        """This function is called to check if a username password combination is
        valid."""
        return username == 'TRAIN' and password == 'TuN3L'


def please_authenticate():
        """Sends a 401 response that enables basic auth"""
        return Response('Could not verify your access level for that URL.\n'
                        'You have to login with proper credentials', 401,
                        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_basic_auth(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
                auth = request.authorization
                if not auth or not check_auth(auth.username, auth.password):
                        return please_authenticate()
                return func(*args, **kwargs)

        return wrapper

@app.route('/login', methods = ['POST'])
@requires_basic_auth
def login():
        session['username'] = request.authorization.username
        return redirect(url_for('hello'))

def requires_user_session(func):
        wraps(func)
        def wrapper(*args, **kwargs):
                if not session.get('username'):
                        return redirect(url_for('login'))
                return func(*args, **kwargs)

        return wrapper

@app.route('/hello')
@requires_user_session
def hellol():
        return render_template('greeting.html', name=session['username'])





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
