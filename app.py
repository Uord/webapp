import sqlite3
from flask import g, Flask
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
    db = get_db()
    data = db.execute('SELECT name FROM tracks').fetchall()
    data = sorted(data)
    return json.dumps(data).encode('utf8')

if __name__ == '__main__':
        app.run(debug=False)