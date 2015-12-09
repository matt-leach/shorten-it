from flask import Flask, request, jsonify, render_template
import flask

from hasher import create_hash
from db import create_redirect, DuplicateError, get_redirect, \
     NotFoundError, add_visit, get_visits, get_browser_counts

import json


app = Flask(__name__)

BANNED_HASHES = ['shorten', 'data']  # ie urls we cannot allow to be hashes


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

    return jsonify({'redirect': "/{}".format(hashed)})


@app.route('/data')
def get_data():
    ''' gets number of counts to /hash '''
    hashed = request.args.get('hash')
    if hashed is None:
        return jsonify({'error': "No 'hashed' parameter"})
    count = get_visits(hashed)
    return jsonify({'views': count})


@app.route('/data/browsers')
def get_browser_data():
    ''' get counts on which browser users are using '''
    hashed = request.args.get('hash')
    if hashed is None:
        return jsonify({'error': "No 'hashed' parameter"})
    data = get_browser_counts(hashed)
    return jsonify({'browsers': data})


@app.route('/<hashed>')
def redirect(hashed):
    ''' redirects from /hash to the url if it's in the database '''
    try:
        redirect_url = get_redirect(hashed)
    except NotFoundError:
        return jsonify({"error": "hash '{}' does not exist".format(hashed)})
    add_visit(hashed, request.user_agent.browser)
    if 'http://' not in redirect_url and 'https://' not in redirect_url:
        redirect_url = 'https://' + redirect_url
    return flask.redirect(redirect_url)  # TODO: fix https://


if __name__ == '__main__':
    app.run(debug=True)
