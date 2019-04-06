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

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, error, status_code=None, payload=None):
        super().__init__(self)
        self.error = error
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.error
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/tracks', methods = ['GET', 'POST'])
def tracks_list():
    if request.method == 'GET':
        return get_tracks()
    else:
        return post_track()


class ValidationForm(Form):
    artist = StringField(validators=[validators.optional()])
    per_page = IntegerField(validators=[validators.optional(),
                                        validators.number_range(min=1)])
    page = IntegerField(validators=[validators.optional(),
                                    validators.number_range(min=1)])


def get_tracks():
    form1 = ValidationForm(request.args)

    if not form1.validate():
        return jsonify(error=form1.errors)

    per_page = form1.data['per_page'] or -1
    limit = per_page

    page = form1.data['page'] or 0
    page_index = page - 1
    offset = page_index * per_page

    if form1.data['artist']:
        db = get_db()
        data = db.execute(
        'SELECT tracks.name, artists.name AS artist FROM tracks '
        'JOIN albums ON tracks.albumid = albums.albumid '
        'JOIN artists ON albums.artistid = artists.artistid '
        'WHERE artists.name = ? '
        'ORDER by tracks.name COLLATE NOCASE '
        'LIMIT ? OFFSET ?;',
        (form1.data['artist'], limit, offset)).fetchall()
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

def post_track():
    db = get_db()
    new_track = request.get_json()
    """ album_id = request.form['album_id']
    media_type_id = request.form['media_type_id']
    genre_id = request.form['genre_id']
    name = request.form['name']
    composer = request.form['composer']
    milliseconds = request.form['milliseconds']
    bytess = request.form['bytes']
    price = request.form['price'] """
    
    album_id = new_track.get('album_id')
    media_type_id = new_track.get('media_type_id')
    genre_id = new_track.get('genre_id')
    name = new_track.get('name')
    composer = new_track.get('composer')
    milliseconds = new_track.get('milliseconds')
    bytess = new_track.get('bytes')
    price = new_track.get('price')

    if album_id is None:
        raise InvalidUsage(f'missing "AlbumID" in request data')
    if media_type_id is None:
        raise InvalidUsage(f'missing "MediaTypeId" in request data')
    if genre_id is None:
        raise InvalidUsage(f'missing "GenreId" in request data')
    if name is None:
        raise InvalidUsage(f'missing "Name" in request data')
    if composer is None:
        raise InvalidUsage(f'missing "Composer" in request data')
    if milliseconds is None:
        raise InvalidUsage(f'missing "Milliseconds" in request data')
    if bytess is None:
        raise InvalidUsage(f'missing "Bytes" in request data')
    if price is None:
        raise InvalidUsage(f'missing "UnitPrice" in request data')

    db.execute('''INSERT INTO tracks (name, albumid, mediatypeid, genreid, composer, milliseconds, bytes, unitprice)
                VALUES (?,?,?,?,?,?,?,?)''',(name, album_id, media_type_id, genre_id, composer, milliseconds, bytess, price))
    db.commit()
    data = db.execute('''SELECT * FROM tracks
                        WHERE trackid = (SELECT MAX(trackid)  FROM tracks)''').fetchone()
    return jsonify(data), 200
@app.route('/genres')
def genres():
    db = get_db()
    genress = db.execute(
        'SELECT genres.name, count(tracks.trackid) '
        'FROM genres '
        'LEFT JOIN tracks ON genres.genreid = tracks.genreid '
        'GROUP BY genres.name;'
    ).fetchall()
    return jsonify(dict(genress))

if __name__ == '__main__':
        app.run(debug=True)