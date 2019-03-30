from functools import wraps
from uuid import uuid4, UUID

from flask import Flask, request, Response, session, redirect, url_for, jsonify, render_template
from flask_basicauth import BasicAuth
from dicttoxml import dicttoxml
import json
import datetime


app = Flask(__name__, template_folder='')
app.counter = 0


app.config['BASIC_AUTH_USERNAME'] = 'TRAIN'
app.config['BASIC_AUTH_PASSWORD'] = 'TuN3L'
app.config['SECRET_KEY'] = 'xwsd23rdsa4'
basic_auth = BasicAuth(app)
mainDict = dict()
empList = []

@app.route('/')
def root():
        return 'Hello, World!'
@app.route('/',methods=['GET'])
def zadanie1w3():
        return Response(status=200)

@app.route('/login',methods=['POST','GET'])
@basic_auth.required
def zadanie2w3():
        session['logged_in'] = True
        return redirect('/hello')


@app.route('/logout',methods=['POST'])
def zadanie3w3():
        if session and session['logged_in']:
                session['logged_in'] = False
                session.pop('logged_in', None)
                return redirect('/')
        return redirect('/login')

@app.route('/hello', methods=['GET'])
def zadanie4w3():
        if not session.get('logged_in', False):
                return redirect('/login')
        return render_template('index.html', user='TRAIN')

@app.route('/trains', methods=['POST','GET'])
def zadanie5w3():
        if not session.get('logged_in', False):
                abort(401)
        if request.method == 'POST':
                empDict = {
                'who' : request.json['who'],
                'where' : request.json['where'],
                'trucks' : int(request.json['trucks']),
                'locomotive' : request.json['locomotive'],
                'date' : request.json['date']}
        
                string = 'uuid_'+ str(len(mainDict)+1)
                dictionary = dict()
                dictionary.update({string : empDict})
                mainDict.update(dictionary)
                return redirect('/trains/'+string+'?format=json')
        
        if request.method == 'GET':
                if request.args.get('format') == 'json':
                return json.dumps(mainDict)
                return dicttoxml(mainDict)

@app.route('/trains/<id>',methods = ['GET','DELETE'])
def zadanie6w3(id):
        if not session.get('logged_in', False):
                abort(401)
        if request.method == 'DELETE':
                if len(mainDict) > 0:
                print(id)
                print(mainDict.get(id))
                mainDict.pop(id)
        if request.method == 'GET':
                if request.args.get('format') == 'json':
                print('id json')
                print(mainDict)
                print(json.dumps(mainDict.get(id)))
                return json.dumps(mainDict.get(id))
                return dicttoxml(mainDict.get(id))


""" @app.route('/login', methods=['GET', 'POST'])
@basic_auth.required
def login():
        session['logged_in'] = True
        return redirect('/hello')



@app.route('/hello')
def hello():
        if not session.get('logged_in', False):
                return redirect('/login')
        return render_template('pozdro.html', name='TRAIN')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
        if request.method == 'GET':
                return redirect('/root')
        del session['logged_in']
        return redirect('/login')
 """


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
