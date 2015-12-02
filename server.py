from flask import Flask, request, jsonify, render_template
import flask

from hasher import create_hash
from db import create_redirect, DuplicateError, get_redirect, NotFoundError, add_visit, get_visits

import json


app = Flask(__name__)

BANNED_HASHES = ['shorten', 'data']  # ie urls we cannot allow to be hashes


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/shorten', methods=['POST'])
def create_short():
    ''' request.data should contain url and (optional) hash '''
    try:
        data = json.loads(request.data)
    except (TypeError, ValueError):
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


@app.route('/data')
def get_data():
    hashed = request.args.get('hash')
    if hashed is None:
        return jsonify({'error': "No 'hashed' parameter"})
    count = get_visits(hashed)
    return jsonify({'views': count})


@app.route('/<hashed>')
def redirect(hashed):
    try:
        redirect_url = get_redirect(hashed)
    except NotFoundError:
        return jsonify({"error": "hash '{}' does not exist".format(hashed)})
    # print request.user_agent.platform, request.user_agent.browser, request.user_agent.version, request.user_agent.language
    add_visit(hashed)
    return flask.redirect('https://' + redirect_url)  # TODO: fix https://


if __name__ == '__main__':
    app.run(debug=True)
