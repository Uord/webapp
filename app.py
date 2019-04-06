from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    url_for,
    jsonify
)
import sqlite3
import json

app = Flask(__name__)

DATABASE = 'chinook.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/tracks')
def tracks_list():
    if request.args.get('artist'):
        db = get_db()
        data = db.execute(
        'SELECT tracks.name, artists.name AS artist FROM tracks '
        'JOIN albums ON tracks.albumid = albums.albumid '
        'JOIN artists ON albums.artistid = artists.artistid '
        'WHERE artists.name = ? '
        'ORDER by tracks.name COLLATE NOCASE;',
        (request.args.get('artist'),)).fetchall()
        data2 = []
        for x in data:
            #data2[x[0]] = x[1]
            data2.append(x[0])
        return jsonify(data2)
    else:
        db = get_db()
        data = db.execute('SELECT name FROM tracks ORDER BY name COLLATE NOCASE').fetchall()
        data2 = []
        for x in data:
            data2.append(x[0])
        return jsonify(data2)



if __name__ == '__main__':
        app.run(debug=False)