from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/method', methods = ['GET', 'POST', 'PUT', 'DELETE'] )
def method():
    return f'{request.method}'

@app.route('/show_data', methods = ['POST'])
def show_data():
    if request.headers['Content-Type'] == 'application/json':
        data = request.get_json()
        return json.dumps(data).encode('utf8')

@app.route('/pretty_print_name', methods = ['POST'])
def print_name():
        data = request.get_json()
        data2 = json.dumps(data).encode('utf8')
        data3 = json.loads(data2)
        return f'Na imię mu {data3.get('name')}, a nazwisko jego {data3.get('surename')}'

if __name__ == '__main__':
    app.run(debug=False)
