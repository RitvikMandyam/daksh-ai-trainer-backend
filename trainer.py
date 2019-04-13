import json

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from tinydb import TinyDB, Query

app = Flask(__name__, static_url_path='/static')
app.config['JSON_SORT_KEYS'] = False
CORS(app)
db = TinyDB('./data.json')


@app.route('/', methods=['GET', 'POST'])
def serve_root():
    if request.method == 'GET':
        with open('./fields.json', 'r') as f:
            data = json.load(f)
            return jsonify(data)
    else:
        data = json.loads(request.form.to_dict()['data'])
        db.insert(data)
        return 'success'


@app.route('/view-cases', methods=['GET', 'POST', 'PUT'])
def serve_view():
    if request.method == 'GET':
        records = db.search(Query().username.exists())
        usernames = set()
        for record in records:
            usernames.add(record['username'])
        return render_template('view-records.html', usernames=usernames)
    elif request.method == 'POST':
        records = db.search(Query().username == request.form['username'])
        return jsonify(records)


@app.route('/bookmarklet', methods=['GET'])
def serve_bookmarklet():
    return render_template('bookmarklet.html')


context = ('/etc/letsencrypt/live/kp.dakshindia.org/cert.pem', '/etc/letsencrypt/live/kp.dakshindia.org/privkey.pem')
app.run(host='0.0.0.0', port=6900, ssl_context=context)
