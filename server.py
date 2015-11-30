from flask import Flask, request, jsonify
import flask
from db import create_redirect, DuplicateError, get_redirect, NotFoundError
import json
from hasher import create_hash

app = Flask(__name__)

BANNED_HASHES = ['shorten', 'data']  # ie urls we cannot allow to be hashes


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
        if hashed in BANNED_HASHES:
            # Cannot create a banned hash
            raise DuplicateError
        create_redirect(url, hashed)
    except DuplicateError:
        return jsonify({'error': "hash '{}' already exists".format(hashed)})
    return jsonify({'redirect': hashed})


@app.route('/<hashed>')
def redirect(hashed):
    try:
        redirect_url = get_redirect(hashed)
    except NotFoundError:
        return jsonify({"error": "hash '{}' does not exist".format(hashed)})
    return flask.redirect('https://' + redirect_url)  # TODO: fix https://


if __name__ == '__main__':
    app.run(debug=True)
