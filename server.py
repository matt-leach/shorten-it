from flask import Flask, request, jsonify
from db import create_redirect, DuplicateError
import json
from hasher import create_hash

app = Flask(__name__)


@app.route('/shorten', methods=['POST'])
def create_short():
    ''' request.data should contain url and (optional) hash '''
    try:
        data = json.loads(request.data)
    except TypeError:
        return jsonify({'error': "Request data must be passed in as a json string"})

    url = data.get('url')
    if url is None:
        return jsonify({'error': "No 'url' parameter present in request data"})

    try:
        hashed = data['hash']
    except KeyError:
        hashed = create_hash(url)
    try:
        create_redirect(url, hashed)
    except DuplicateError:
        return jsonify({'error': "hash '{}' already exists".format(hashed)})
    return jsonify({'redirect': hashed})


@app.route('/data', methods=['POST'])
def load_data():
    content = request.get_json(force=True)
    return jsonify(content)


if __name__ == '__main__':
    app.run(debug=True)
