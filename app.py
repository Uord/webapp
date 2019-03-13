from flask import Flask
from flask import request

app = Flask(__name__)



@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/method', methods = ['POST', 'PUT' 'GET'])
def method():
    return f'{request.methods}'


if __name__ == '__main__':
    app.run(debug=False)
