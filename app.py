from flask import Flask, request, session, redirect, abort, Response, render_template, url_for
from flask_basicauth import BasicAuth
from dicttoxml import dicttoxml
import json
import datetime

app = Flask(__name__, template_folder='')
i = 0
mainDict = dict()
empList = []

app.config['BASIC_AUTH_USERNAME'] = 'TRAIN'
app.config['BASIC_AUTH_PASSWORD'] = 'TuN3L'
app.config['SECRET_KEY'] = 'VerySecretRandomString'
basic_auth = BasicAuth(app)

@app.route('/show_data', methods=['POST'])
def zadanie3():
    data = request.data
    return data

@app.route('/method', methods=['GET','POST','PUT','DELETE'])
def zadanie2():
    return f'{request.method}'

@app.route('/')
def zadanie1():
    return 'Hello, World!'


@app.route('/pretty_print_name', methods = ['POST'])
def task4():
    data = request.get_json()
    return f"Na imię mu {data['name']}, a nazwisko jego {data['surename']}"

@app.route('/counter')
def zadanie5():
    global i
    i += 1
    return f"{i}"


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
    return render_template('pozdro.html', name='TRAIN')

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


@app.route('/trains/<trainId>',methods = ['GET','DELETE'])
def zadanie6w3(trainId):
    if not session.get('logged_in', False):
        abort(401)
    if request.method == 'DELETE':
        if len(mainDict) > 0:
            if trainId in mainDict:
                print(trainId)
                print(mainDict.get(trainId))
                print('pop')
                mainDict.pop(trainId)
                print(mainDict.get(trainId))
                return Response(status=200)
            return Response(status=404)
        return Response(status=404)
    if request.method == 'GET':
        if request.args.get('format') == 'json':
            print('id json')
            print(mainDict)
            print(json.dumps(mainDict.get(trainId)))
            return json.dumps(mainDict.get(trainId))
        print(dicttoxml(mainDict.get(trainId)))
        return dicttoxml(mainDict.get(trainId))