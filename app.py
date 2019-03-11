from flask import Flask
from flask import request
import time
app = Flask(__name__)



@app.route('/')
def hello():
    return 'Siemano, Ola!'


@app.route('/user-agent')
def user_info():
    return f'browser: {request.user_agent.browser} os: {request.user_agent.platform} '


@app.route('/request')
def request_info():
    return f'request method: {request.method} url: {request.url} headers: {request.headers}'


if __name__ == '__main__':
    app.run(debug=False)
