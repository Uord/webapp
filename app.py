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
from wtforms import Form, StringField, validators, IntegerField

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

    form = ValidationForm(request.args)

    if not form.validate():
        return jsonify(error=form.errors)

    per_page = form.data['per_page'] or -1
    limit = per_page

    page = form.data['page'] or 0
    page_index = page - 1
    offset = page_index * per_page

    if form.data['artist']:
        db = get_db()
        data = db.execute(
        'SELECT tracks.name, artists.name AS artist FROM tracks '
        'JOIN albums ON tracks.albumid = albums.albumid '
        'JOIN artists ON albums.artistid = artists.artistid '
        'WHERE artists.name = ? '
        'ORDER by tracks.name COLLATE NOCASE '
        'LIMIT ? OFFSET ?;',
        (form.data['artist'], limit, offset)).fetchall()
        data2 = []
        for x in data:
            #data2[x[0]] = x[1]
            data2.append(x[0])
        return jsonify(data2)
    else:
        db = get_db()
        data = db.execute('SELECT name FROM tracks ORDER BY name COLLATE NOCASE LIMIT  ? OFFSET ?;', (limit, offset)).fetchall()
        data2 = []
        for x in data:
            data2.append(x[0])
        return jsonify(data2)

class ValidationForm(Form):
    artist = StringField(validators=[validators.optional()])
    per_page = IntegerField(validators=[validators.optional(),
                                        validators.number_range(min=1)])
    page = IntegerField(validators=[validators.optional(),
                                    validators.number_range(min=1)])



if __name__ == '__main__':
        app.run(debug=False)